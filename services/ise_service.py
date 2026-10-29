import base64
import os
from pathlib import Path

from xfyunsdkspeech.ise_client import IseClient

from utils.xml_parser import parse_ise_xml


def _create_ise_client(category: str) -> IseClient:
    app_id = os.getenv("APP_ID")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    if not all([app_id, api_key, api_secret]):
        raise ValueError("APP_ID/API_KEY/API_SECRET 未完整配置。")
    return IseClient(
        app_id=app_id,
        api_key=api_key,
        api_secret=api_secret,
        aue="raw",
        group="pupil",
        ent="cn_vip",
        category=category,
    )


class ISEService:
    def __init__(self) -> None:
        self.client = _create_ise_client("read_sentence")

    def evaluate(self, pcm_path: Path, question_text: str) -> dict:
        xml_result = ""
        with open(pcm_path, "rb") as pcm_file:
            for chunk in self.client.stream("\uFEFF" + question_text, pcm_file):
                if chunk.get("data"):
                    xml_result += base64.b64decode(chunk["data"]).decode("utf-8")

        if not xml_result:
            raise ValueError("ISE 未返回评测 XML 结果。")

        parsed = parse_ise_xml(xml_result, category="read_sentence")
        return parsed

    def evaluate_chapter(self, pcm_path: Path, reference_text: str) -> dict:
        """
        篇章朗读评测，用于命题说话场景。
        参考文本通常为 ASR 转写结果，用于评估发音与文本的匹配度。
        """
        chapter_client = _create_ise_client("read_chapter")
        xml_result = ""
        with open(pcm_path, "rb") as pcm_file:
            for chunk in chapter_client.stream("\uFEFF" + reference_text, pcm_file):
                if chunk.get("data"):
                    xml_result += base64.b64decode(chunk["data"]).decode("utf-8")

        if not xml_result:
            raise ValueError("ISE 未返回评测 XML 结果。")

        return parse_ise_xml(xml_result, category="read_chapter")
