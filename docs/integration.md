# 前后端交互流程

本文说明前端如何调用后端、代理配置、流式处理与错误处理。

## 请求链路

1. 用户在前端选择题目、填写/沿用指导重点，录音或上传音频后点击提交。
2. 前端将当前题目的 `content` 作为 `question_text`，将输入框内容（或题目 `prompt`/`guidance`）作为 `guidance`，与音频文件一起以 `multipart/form-data` 提交到 `/api/evaluation/`。
3. 开发环境下，Vite 将 `http://localhost:3000/api/*` 代理到 `http://127.0.0.1:8000/api/*`，因此实际请求发往后端 8000 端口。
4. 后端返回 `Content-Type: application/x-ndjson` 的流式响应，前端使用 `fetch` + `ReadableStream` 逐行解析 JSON 并更新 UI。

## 代理配置

- **开发**：`frontend/vite.config.ts` 中 `server.proxy['/api']` 指向 `http://127.0.0.1:8000`，前端仅需写相对路径 `/api/evaluation/`。
- **生产**：需在 Nginx 等反向代理中将 `/api` 转发到 Django 后端，或前端配置与后端同域。

## 流式处理

1. 前端 `submitEvaluation()`（`src/api/evaluation.ts`）使用 `fetch` 请求接口，通过 `response.body.getReader()` 读取流。
2. 按行拆分缓冲，每行解析为 JSON，根据 `type` 分发：
   - `evaluation` → 写入评测结果状态，展示评分卡片
   - `feedback_chunk` → 追加到当前反馈文案，流式展示
   - `done` → 结束加载、清理状态
   - `error` → 提示 `detail`
   - `info` → 可选打日志
3. 若请求本身 4xx/5xx，`response.ok` 为 false，前端按错误响应 body 提示用户。

## 数据对应关系

| 前端 | 后端 |
|------|------|
| 当前题目 `content` | `question_text` |
| 输入框内容 或 题目 `prompt`/`guidance` | `guidance` |
| 录音或上传的 File | `audio` |
| 评测结果（evaluation.data） | 展示总分、准确度、流畅度等 |
| feedback_chunk 拼接结果 | 展示为 LLM 反馈文本 |

## 错误与边界

- **网络/超时**：前端 catch 后提示“提交失败”等。
- **后端返回 error 类型**：展示 `chunk.detail`。
- **未配置星火**：后端仍返回 `evaluation` 与 `done`，无 `feedback_chunk`，前端仅显示评测结果。
