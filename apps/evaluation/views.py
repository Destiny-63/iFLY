import json
from tempfile import TemporaryDirectory

from django.http import StreamingHttpResponse
from dotenv import load_dotenv
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.evaluation.serializers import (
    EvaluationRequestSerializer,
    TopicSpeakingRequestSerializer,
)
from services.audio_processor import AudioFormatError, AudioProcessor
from services.ise_service import ISEService
from services.lfasr_service import LFASRService, LFASRServiceError
from services.spark_service import SparkService
from services.topic_scoring import compute_time_penalty

load_dotenv()


class EvaluationAPIView(APIView):
    """
    语音评测接口
    
    接收音频文件（.mp3 或 .pcm）和题目信息，返回 ISE 评测结果和 LLM 生成的反馈建议。
    支持流式响应，先返回评测结果，再流式返回 LLM 反馈。
    """
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        tags=["评测"],
        summary="提交音频进行语音评测",
        description="""
        提交音频文件进行普通话口语评测，返回详细的评分结果和 LLM 生成的改进建议。
        
        **流程：**
        1. 接收音频文件（支持 .mp3 和 .pcm 格式）
        2. 如果是 .mp3，自动转换为 PCM 格式（16kHz/16bit/单声道）
        3. 调用讯飞 ISE API 进行评测
        4. 基于评测结果，调用星火大模型生成个性化反馈（如果已配置）
        
        **响应格式：**
        返回流式 NDJSON 格式，每行一个 JSON 对象：
        - `{"type": "evaluation", "data": {...}}` - 评测结果
        - `{"type": "feedback_chunk", "data": "..."}` - LLM 反馈片段（流式）
        - `{"type": "done"}` - 完成标记
        - `{"type": "error", "detail": "..."}` - 错误信息
        """,
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "audio": {
                        "type": "string",
                        "format": "binary",
                        "description": "音频文件，支持 .mp3 或 .pcm 格式",
                    },
                    "question_text": {
                        "type": "string",
                        "description": "评测题目文本（中文）",
                        "example": "今天天气怎么样",
                    },
                    "guidance": {
                        "type": "string",
                        "description": "希望 LLM 重点关注的内容",
                        "example": "请重点关注声调和流畅度",
                    },
                },
                "required": ["audio", "question_text", "guidance"],
            }
        },
        responses={
            200: {
                "description": "成功返回流式响应",
                "content": {
                    "application/x-ndjson": {
                        "example": [
                            '{"type": "evaluation", "data": {"total_score": 92.51, "accuracy_score": 100.0, "fluency_score": 87.62, "integrity_score": 100.0}}',
                            '{"type": "feedback_chunk", "data": "总体评价：..."}',
                            '{"type": "done"}',
                        ]
                    }
                },
            },
            400: {
                "description": "请求参数错误",
                "content": {
                    "application/json": {
                        "example": {"detail": "仅支持 .mp3 或 .pcm 文件。"}
                    }
                },
            },
            502: {
                "description": "ISE 评测服务错误",
                "content": {
                    "application/json": {
                        "example": {"detail": "ISE 评测失败: ..."}
                    }
                },
            },
        },
        examples=[
            OpenApiExample(
                "成功请求示例",
                value={
                    "audio": "(binary file)",
                    "question_text": "今天天气怎么样",
                    "guidance": "请重点关注声调和流畅度",
                },
            ),
        ],
    )
    def post(self, request):
        serializer = EvaluationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        payload = serializer.validated_data
        question_text = payload["question_text"]
        guidance = payload["guidance"]
        uploaded_audio = payload["audio"]

        processor = AudioProcessor()
        with TemporaryDirectory(prefix="eval_") as _:
            source_path = processor.save_upload_to_temp(uploaded_audio)
            pcm_path = source_path
            try:
                pcm_path = processor.ensure_pcm(source_path)
                evaluation_result = ISEService().evaluate(pcm_path, question_text)
            except (AudioFormatError, ValueError) as exc:
                return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as exc:
                return Response(
                    {"detail": f"ISE 评测失败: {exc}"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )
            finally:
                processor.cleanup_temp_file(source_path)
                if pcm_path != source_path:
                    processor.cleanup_temp_file(pcm_path)

        def stream_generator():
            # 首包先返回评测结构化结果，便于前端同步渲染评分卡片。
            yield json.dumps(
                {"type": "evaluation", "data": evaluation_result}, ensure_ascii=False
            ) + "\n"
            
            # 尝试调用星火 API 生成反馈（如果配置了的话）
            try:
                spark_service = SparkService()
                for text_chunk in spark_service.stream_feedback(
                    evaluation_result, question_text, guidance
                ):
                    yield (
                        json.dumps(
                            {"type": "feedback_chunk", "data": text_chunk},
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
                yield json.dumps({"type": "done"}, ensure_ascii=False) + "\n"
            except ValueError as exc:
                # 星火 API 未配置，跳过反馈生成
                if "SPARK_API" in str(exc):
                    yield (
                        json.dumps(
                            {
                                "type": "info",
                                "detail": "星火 API 未配置，仅返回评测结果。如需 LLM 反馈，请在 .env 中配置 SPARK_API_KEY 和 SPARK_API_URL。",
                            },
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
                    yield json.dumps({"type": "done"}, ensure_ascii=False) + "\n"
                else:
                    yield (
                        json.dumps(
                            {"type": "error", "detail": str(exc)},
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
            except Exception as exc:
                yield (
                    json.dumps(
                        {"type": "error", "detail": f"星火调用失败: {exc}"},
                        ensure_ascii=False,
                    )
                    + "\n"
                )

        return StreamingHttpResponse(
            streaming_content=stream_generator(),
            content_type="application/x-ndjson; charset=utf-8",
            status=status.HTTP_200_OK,
        )


class TopicSpeakingAPIView(APIView):
    """
    命题说话评测接口

    接收话题和音频，用户围绕话题自由演讲，返回四维度评分及 LLM 指导建议。
    流程：ASR 转写 -> 时长计算 -> ISE 篇章评测 -> LLM 综合评分。
    """
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        tags=["评测"],
        summary="命题说话评测",
        description="""
        针对给定话题，用户围绕话题自由演讲，系统给出四维度评分及指导建议。

        **评分维度：**
        - 语音标准程度（25分）
        - 词汇语法规范程度（10分）
        - 自然流畅程度（5分）
        - 时间惩罚（缺时扣分）

        **流程：** 音频转写 -> ISE 发音评测 -> LLM 综合评分

        **注意：** 转写为异步，3 分钟音频约需 3-6 分钟返回，请保持连接。
        """,
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "audio": {"type": "string", "format": "binary"},
                    "topic": {"type": "string", "description": "话题，如：我喜欢的季节"},
                },
                "required": ["audio", "topic"],
            }
        },
        responses={200: {"description": "流式 NDJSON 响应"}},
    )
    def post(self, request):
        serializer = TopicSpeakingRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        topic = serializer.validated_data["topic"]
        uploaded_audio = serializer.validated_data["audio"]

        processor = AudioProcessor()
        with TemporaryDirectory(prefix="topic_") as _:
            source_path = processor.save_upload_to_temp(uploaded_audio)
            pcm_path = source_path
            try:
                pcm_path = processor.ensure_pcm(source_path)
                duration_seconds = processor.get_duration_seconds(pcm_path)
            except (AudioFormatError, ValueError) as exc:
                return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as exc:
                return Response(
                    {"detail": f"音频处理失败: {exc}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ASR 转写（使用原始文件上传，支持 mp3/pcm）
            try:
                lfasr = LFASRService()
                transcript = lfasr.transcribe(source_path, int(duration_seconds))
            except ValueError as exc:
                return Response(
                    {"detail": str(exc)},
                    status=status.HTTP_502_BAD_GATEWAY,
                )
            except LFASRServiceError as exc:
                return Response(
                    {"detail": f"语音转写失败: {exc}"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            # ISE 篇章评测（转写文本足够长时）
            ise_result = None
            if transcript and len(transcript.strip()) >= 20:
                try:
                    ise_result = ISEService().evaluate_chapter(pcm_path, transcript)
                except Exception:
                    pass  # 忽略 ISE 失败，继续用 LLM

            time_penalty = compute_time_penalty(duration_seconds)

            evaluation_data = {
                "topic": topic,
                "duration_seconds": round(duration_seconds, 1),
                "transcript": transcript,
                "ise_result": ise_result,
                "time_penalty": time_penalty,
            }

            def stream_generator():
                try:
                    yield json.dumps(
                        {"type": "evaluation", "data": evaluation_data},
                        ensure_ascii=False,
                    ) + "\n"

                    spark = SparkService()
                    buffer = ""
                    parsed_psc = False
                    for chunk in spark.stream_topic_feedback(
                        topic, transcript, duration_seconds, ise_result, time_penalty
                    ):
                        buffer += chunk
                        if not parsed_psc and "\n" in buffer:
                            idx = buffer.find("\n")
                            json_line = buffer[:idx]
                            rest = buffer[idx + 1 :]
                            buffer = ""
                            parsed_psc = True
                            try:
                                d = json.loads(json_line.strip())
                                if "psc_score" in d:
                                    yield (
                                        json.dumps(
                                            {
                                                "type": "evaluation_update",
                                                "data": {"psc_score": d["psc_score"]},
                                            },
                                            ensure_ascii=False,
                                        )
                                        + "\n"
                                    )
                            except json.JSONDecodeError:
                                pass
                            if rest:
                                yield (
                                    json.dumps(
                                        {"type": "feedback_chunk", "data": rest},
                                        ensure_ascii=False,
                                    )
                                    + "\n"
                                )
                        elif parsed_psc:
                            yield (
                                json.dumps(
                                    {"type": "feedback_chunk", "data": chunk},
                                    ensure_ascii=False,
                                )
                                + "\n"
                            )
                            buffer = ""
                    if buffer:
                        yield (
                            json.dumps(
                                {"type": "feedback_chunk", "data": buffer},
                                ensure_ascii=False,
                            )
                            + "\n"
                        )
                    yield json.dumps({"type": "done"}, ensure_ascii=False) + "\n"
                except ValueError as exc:
                    if "SPARK" in str(exc):
                        yield (
                            json.dumps(
                                {
                                    "type": "info",
                                    "detail": "星火 API 未配置，仅返回评测结果。",
                                },
                                ensure_ascii=False,
                            )
                            + "\n"
                        )
                    else:
                        yield (
                            json.dumps(
                                {"type": "error", "detail": str(exc)},
                                ensure_ascii=False,
                            )
                            + "\n"
                        )
                    yield json.dumps({"type": "done"}, ensure_ascii=False) + "\n"
                except Exception as exc:
                    yield (
                        json.dumps(
                            {"type": "error", "detail": f"LLM 调用失败: {exc}"},
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
                finally:
                    processor.cleanup_temp_file(source_path)
                    if pcm_path != source_path:
                        processor.cleanup_temp_file(pcm_path)

            return StreamingHttpResponse(
                streaming_content=stream_generator(),
                content_type="application/x-ndjson; charset=utf-8",
                status=status.HTTP_200_OK,
            )
