import xml.etree.ElementTree as ET


def parse_ise_xml(xml_text: str, category: str | None = None) -> dict:
    """
    解析 ISE 评测 XML 结果。

    Args:
        xml_text: XML 字符串
        category: 可选，指定题型。若为 None，则自动检测 read_chapter 或 read_sentence。
    """
    root = ET.fromstring(xml_text)
    read_node = None

    if category == "read_chapter":
        read_node = root.find(".//rec_paper/read_chapter")
    elif category == "read_sentence":
        read_node = root.find(".//rec_paper/read_sentence")
        if read_node is None:
            read_node = root.find(".//read_sentence/read_sentence")
    else:
        # 自动检测：优先 read_chapter，再 read_sentence
        read_node = root.find(".//rec_paper/read_chapter")
        if read_node is None:
            read_node = root.find(".//rec_paper/read_sentence")
        if read_node is None:
            read_node = root.find(".//read_sentence/read_sentence")

    if read_node is None:
        raise ValueError("ISE 返回结果格式异常，缺少 read_chapter 或 read_sentence 节点。")

    # 中文 read_chapter 使用 phone_score，无 accuracy_score；read_sentence 可能有 accuracy_score
    accuracy = _to_float(read_node.attrib.get("accuracy_score"))
    if accuracy is None:
        accuracy = _to_float(read_node.attrib.get("phone_score"))

    result = {
        "total_score": _to_float(read_node.attrib.get("total_score")),
        "accuracy_score": accuracy,
        "fluency_score": _to_float(read_node.attrib.get("fluency_score")),
        "integrity_score": _to_float(read_node.attrib.get("integrity_score")),
        "tone_score": _to_float(read_node.attrib.get("tone_score")),
        "phone_score": _to_float(read_node.attrib.get("phone_score")),
        "raw_xml": xml_text,
    }
    return result


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None
