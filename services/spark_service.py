import json
import os
from typing import Generator

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


class SparkService:
    def __init__(self) -> None:
        # 优先使用 SPARK_API_KEY，如果没有则使用 API_PASSWORD（兼容旧配置）
        self.api_key = os.getenv("SPARK_API_KEY") or os.getenv("API_PASSWORD")
        self.base_url = os.getenv("SPARK_API_URL")
        self.model = os.getenv("SPARK_MODEL", "spark-x")

        if not self.api_key or not self.base_url:
            raise ValueError("SPARK_API_KEY/SPARK_API_URL 未完整配置。")

        # 确保 base_url 以 / 结尾（LangChain 需要）
        if not self.base_url.endswith("/"):
            self.base_url += "/"

        self.client = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=0.2,
            streaming=True,
        )

    def stream_feedback(
        self, evaluation_result: dict, question_text: str, guidance: str
    ) -> Generator[str, None, None]:
        system_prompt = (
            "你是一名专业的普通话口语训练教练，擅长分析发音问题并提供针对性指导。"
            "你的任务是：\n"
            "1. 基于评测结果分析发音优缺点\n"
            "2. 提供具体、可执行的改进建议\n"
            "3. 重点关注用户指定的训练方向\n"
            "4. 用鼓励性的语言，帮助学员建立信心\n\n"
            "输出要求：语言简洁明了，条理清晰，每一条建议都要具体可操作。"
        )
        
        # 提取关键评分信息，便于 LLM 理解
        total_score = evaluation_result.get("total_score", 0)
        accuracy = evaluation_result.get("accuracy_score", 0)
        fluency = evaluation_result.get("fluency_score", 0)
        integrity = evaluation_result.get("integrity_score", 0)
        
        user_prompt = (
            f"【评测题目】\n{question_text}\n\n"
            f"【用户关注重点】\n{guidance}\n\n"
            f"【评测结果详情】\n"
            f"- 总分：{total_score:.2f}分（满分100分）\n"
            f"- 准确度：{accuracy:.2f}分（发音准确性）\n"
            f"- 流畅度：{fluency:.2f}分（语流顺畅程度）\n"
            f"- 完整度：{integrity:.2f}分（内容完整程度）\n\n"
            f"【完整评测数据】\n{json.dumps(evaluation_result, ensure_ascii=False, indent=2)}\n\n"
            f"【请提供以下内容】\n"
            f"1. **总体评价**（2-3句话）：\n"
            f"   - 总结本次发音表现\n"
            f"   - 指出最突出的优点和需要改进的地方\n\n"
            f"2. **针对性建议**（3-5条，每条1-2句话）：\n"
            f"   - 必须围绕用户关注的重点：{guidance}\n"
            f"   - 每条建议要具体可操作，不要泛泛而谈\n"
            f"   - 可以结合具体评分指出问题（如：流畅度较低，建议...）\n\n"
            f"3. **下一步练习目标**（1条具体目标）：\n"
            f"   - 基于当前评测结果，设定一个明确的改进目标\n"
            f"   - 目标要具体、可衡量\n\n"
            f"请直接开始输出，不要重复题目和评测数据。"
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        for chunk in self.client.stream(messages):
            content = getattr(chunk, "content", "")
            if content:
                yield content

    def stream_topic_feedback(
        self,
        topic: str,
        transcript: str,
        duration_seconds: float,
        ise_result: dict | None,
        time_penalty: dict,
    ) -> Generator[str, None, None]:
        """
        命题说话评测的 LLM 反馈。

        四维度：语音标准(25)、词汇语法(10)、自然流畅(5)、时间惩罚。
        维度四由代码计算，其余由 LLM 评估。
        """
        rubric = """
【命题说话评分细则】

维度一：语音标准程度（25分）
- 一档(扣0-2分)：语音标准，语调自然，失误≤3次
- 二档(扣3-4分)：错误≤10次，轻微方音
- 三档(扣5-6分)：错误10-15次，方音较明显
- 四档(扣7-9分)：错误>15次，方音明显
- 五档(扣10-14分)：方音重，影响理解
- 六档(扣15-25分)：语音极不标准

维度二：词汇语法规范程度（10分）
- 一档：不扣分
- 二档(扣1-2分)：方言/语法错误1-2次
- 三档(扣3-4分)：3次及以上

维度三：自然流畅程度（5分）
- 一档：不扣分，自然流畅
- 二档(扣0.5-1分)：有背稿感
- 三档(扣2-3分)：语流不畅、重复、停顿多

维度四：时间惩罚（已由系统计算）：{time_deduct}分 - {time_reason}
"""
        time_part = rubric.format(
            time_deduct=time_penalty.get("deduct", 0),
            time_reason=time_penalty.get("reason", ""),
        )

        ise_info = ""
        if ise_result:
            acc = ise_result.get("accuracy_score") or ise_result.get("phone_score")
            flu = ise_result.get("fluency_score")
            ise_info = (
                f"\n【ISE 发音评测参考】\n"
                f"- 准确度/声韵分：{acc}\n"
                f"- 流畅度：{flu}\n"
                f"（可作为维度一语音标准的参考）\n"
            )

        system_prompt = (
            "你是普通话水平测试命题说话部分的专业考官。"
            "根据转写文本、时长、ISE 发音评测结果，按四维度给出评分和指导建议。"
            "输出要求：简洁、具体、可操作。"
        )

        user_prompt = (
            f"【话题】\n{topic}\n\n"
            f"【用户转写文本】\n{transcript or '（转写为空）'}\n\n"
            f"【时长】{duration_seconds:.1f} 秒（要求满 180 秒）\n"
            f"{ise_info}\n"
            f"{time_part}\n\n"
            f"【重要】请严格按以下顺序输出：\n\n"
            f"第一步：在回复的【第一行】且【仅第一行】输出一个 JSON 对象，格式为：\n"
            f'{{"psc_score":{{"dim1_deduct":N,"dim2_deduct":N,"dim3_deduct":N,"total":N}}}}\n'
            f"其中 dim1_deduct=维度一语音标准扣分(0-25)，dim2_deduct=维度二词汇语法扣分(0-4)，dim3_deduct=维度三自然流畅扣分(0-3)，total=40减去三个维度扣分再减去时间惩罚{time_penalty.get('deduct', 0)}后的最终得分。\n\n"
            f"第二步：换行后输出正文，包含：\n"
            f"1. **各维度扣分**：维度一、二、三的档位与扣分（维度四已给出）\n"
            f"2. **总体评价**（2-3 句）\n"
            f"3. **改进建议**（3-5 条，具体可操作）\n\n"
            f"直接开始输出，第一行必须是上述 JSON，不要重复题目。"
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        for chunk in self.client.stream(messages):
            content = getattr(chunk, "content", "")
            if content:
                yield content
