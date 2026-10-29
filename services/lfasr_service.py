"""
讯飞录音文件转写（标准版）服务

使用官方 xfyunsdkspeech.LFasrClient，需配置 APP_ID 和 API_SECRET。
请在讯飞控制台开通「语音转写」服务。
参考：https://www.xfyun.cn/doc/asr/ifasr_new/API.html
"""

import json
import os
import time
from pathlib import Path

from xfyunsdkspeech.lfasr_client import LFasrClient
from xfyunsdkcore.model.lfasr_model import UploadParam


POLL_INTERVAL = 5  # 轮询间隔（秒），建议 5 秒避免频率限制
MAX_POLL_COUNT = 120  # 最多轮询约 10 分钟


class LFASRServiceError(Exception):
    pass


def _extract_transcript_from_order_result(order_result_str: str) -> str:
    """
    从 orderResult JSON 中提取转写文本。
    结构：lattice[].json_1best -> st.rt[].ws[].cw[].w
    """
    try:
        data = json.loads(order_result_str)
    except json.JSONDecodeError:
        return ""

    lattice = data.get("lattice") or data.get("lattice2") or []
    parts = []

    for item in lattice:
        json_1best = item.get("json_1best")
        if json_1best is None:
            continue
        if isinstance(json_1best, str):
            try:
                json_1best = json.loads(json_1best)
            except json.JSONDecodeError:
                continue

        st = json_1best.get("st") if isinstance(json_1best, dict) else None
        if not st:
            continue

        rt = st.get("rt") or []
        for seg in rt:
            ws_list = seg.get("ws") or []
            for ws in ws_list:
                cw_list = ws.get("cw") or []
                for cw in cw_list:
                    w = cw.get("w", "").strip()
                    if w:
                        parts.append(w)

    return "".join(parts)


class LFASRService:
    def __init__(self) -> None:
        # 语音转写使用独立配置，不覆盖 ISE/大模型 的 APP_ID、API_SECRET
        self.app_id = os.getenv("LFASR_APP_ID") or os.getenv("APP_ID")
        self.secret_key = os.getenv("LFASR_SECRET_KEY")
        if not self.app_id or not self.secret_key:
            raise ValueError(
                "LFASR_SECRET_KEY 未配置。"
                "请在 .env 中配置语音转写服务的 SecretKey（控制台-语音转写-服务管理）。"
            )
        self.client = LFasrClient(
            app_id=self.app_id,
            secret_key=self.secret_key,
        )

    def transcribe(self, audio_path: Path, duration_seconds: int) -> str:
        """
        上传音频并轮询获取转写文本。

        Args:
            audio_path: 音频文件路径（支持 mp3、wav、pcm 等）
            duration_seconds: 音频时长（秒）

        Returns:
            转写文本
        """
        file_path = str(audio_path.resolve())
        file_name = audio_path.name or "audio.mp3"
        file_size = audio_path.stat().st_size

        param = UploadParam(
            audioMode="fileStream",
            fileName=file_name,
            fileSize=file_size,
            duration=duration_seconds,
            language="cn",
        )

        upload_resp = self.client.upload(param.to_dict(), file_path)
        upload_data = json.loads(upload_resp)

        if upload_data.get("code") != "000000":
            desc = upload_data.get("descInfo", "unknown")
            code = upload_data.get("code", "")
            raise LFASRServiceError(f"上传失败: {desc} (code={code})")

        order_id = upload_data.get("content", {}).get("orderId")
        if not order_id:
            raise LFASRServiceError("上传成功但未返回 orderId")

        # 轮询获取结果
        for _ in range(MAX_POLL_COUNT):
            time.sleep(POLL_INTERVAL)

            result_resp = self.client.get_result({"orderId": order_id})
            result_data = json.loads(result_resp)

            if result_data.get("code") != "000000":
                continue

            content = result_data.get("content", {})
            order_info = content.get("orderInfo", {})
            status = order_info.get("status")

            if status == -1:
                fail_type = order_info.get("failType", "unknown")
                raise LFASRServiceError(f"转写失败: failType={fail_type}")

            if status == 4:
                order_result = content.get("orderResult", "")
                if order_result:
                    return _extract_transcript_from_order_result(order_result)
                return ""

        raise LFASRServiceError("转写超时，请稍后重试")
