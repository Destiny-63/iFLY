# API 接口说明

当前后端对外提供评测流式接口，用于上传音频、题目与指导重点，并返回 ISE 评测结果与 LLM 反馈。

## 评测接口

### POST `/api/evaluation/`

提交音频进行普通话口语评测，返回流式 NDJSON。

**Content-Type**：`multipart/form-data`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `audio` | File | 是 | 音频文件，支持 .mp3 或 .pcm |
| `question_text` | string | 是 | 题目文本（中文），与前端当前题目一致 |
| `guidance` | string | 是 | 希望 LLM 重点指导的内容（可与题目配置中的 guidance/prompt 一致） |

**响应**：`Content-Type: application/x-ndjson`，每行一个 JSON 对象。

| type | 说明 |
|------|------|
| `evaluation` | ISE 评测结果，`data` 为对象，含 `total_score`、`accuracy_score`、`fluency_score`、`integrity_score` 等 |
| `feedback_chunk` | LLM 反馈的一段文本，`data` 为字符串，前端需按顺序拼接 |
| `done` | 流结束，无 `data` |
| `error` | 错误，`detail` 为错误信息 |
| `info` | 提示信息，`detail` 为说明 |

**示例（按行）**：

```json
{"type": "evaluation", "data": {"total_score": 92.51, "accuracy_score": 100.0, "fluency_score": 87.62, "integrity_score": 100.0}}
{"type": "feedback_chunk", "data": "总体"}
{"type": "feedback_chunk", "data": "评价："}
{"type": "feedback_chunk", "data": "..."}
{"type": "done"}
```

**错误响应**（非流式，HTTP 4xx/5xx）：

- 400：如仅支持 .mp3 或 .pcm、缺少参数等，body 为 `{"detail": "..."}`

## 联调示例

### cURL（Linux / macOS）

```bash
curl -N -X POST "http://127.0.0.1:8000/api/evaluation/" \
  -F "audio=@resources/ise/read_sentence_cn.mp3" \
  -F "question_text=今天天气怎么样" \
  -F "guidance=请重点关注声调和流畅度"
```

### PowerShell（Windows）

```powershell
curl.exe -N -X POST "http://127.0.0.1:8000/api/evaluation/" `
  -F "audio=@resources/ise/read_sentence_cn.mp3" `
  -F "question_text=今天天气怎么样" `
  -F "guidance=请重点关注声调和流畅度"
```

### Postman

- Method: **POST**
- URL: `http://127.0.0.1:8000/api/evaluation/`
- Body → **form-data**：`audio`（File）、`question_text`（Text）、`guidance`（Text）
- 流式结果在 Postman 中可能不如终端直观，建议用 `curl -N` 验证

## 在线文档

启动后端后可通过以下地址查看与调试：

- **Swagger UI**：http://127.0.0.1:8000/api/docs/
- **ReDoc**：http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema**：http://127.0.0.1:8000/api/schema/
