# 软件设计概览

本文简要说明系统架构与模块职责，便于二次开发与维护。

## 整体架构

- **前端**：Vue3 单页应用，题型与题目来自静态 JSON，评测与反馈通过 REST 流式接口与后端通信。
- **后端**：Django + DRF，提供评测接口；内部调用讯飞 ISE 做语音评测、星火做 LLM 反馈，音频格式由本地服务统一处理。

```
┌─────────────────┐     /api/evaluation/      ┌─────────────────┐
│  Vue3 前端      │ ─── multipart + 流式 ───► │  Django 后端    │
│  (题型/题目/    │ ◄── NDJSON 流式响应 ────  │  (评测视图 +    │
│   录音/上传)    │                           │   ISE + 星火)   │
└─────────────────┘                           └─────────────────┘
        │                                              │
        │ 题目 JSON                                     │ .env
        ▼                                              ▼
  public/data/questions.json                    讯飞/星火 API
```

## 后端模块

| 模块 | 职责 |
|------|------|
| `apps.evaluation.views` | 接收上传、校验参数、协调音频处理与评测、组装流式响应 |
| `apps.evaluation.serializers` | 校验 `audio`、`question_text`、`guidance` |
| `services.audio_processor` | mp3 → 16kHz/16bit 单声道 PCM |
| `services.ise_service` | 调用讯飞 ISE，返回评测结果 |
| `services.spark_service` | 调用星火，流式生成反馈文本 |

评测流程：接收文件 → 可选转码 → ISE 评测 → 若配置星火则流式请求星火并逐块写入响应 → 发送 `evaluation` / `feedback_chunk` / `done`。

## 前端模块

| 模块 | 职责 |
|------|------|
| `views/Home.vue` | 主页面：题型路由、题目展示、指导重点输入、录音/上传、提交、评测结果与 LLM 反馈展示、收藏 |
| `composables/useQuestionBank` | 请求 `/data/questions.json`，按题型提供题目列表，失败时回退 mock |
| `composables/useAudioRecorder` | 录音、生成可上传的音频 Blob/File |
| `api/evaluation.ts` | 调用 `/api/evaluation/`，解析 NDJSON 流并回调各 type |
| `types/questions.ts` | 题目类型定义与多语种解析（title/difficulty/tags） |
| `router` | `/question-type/:type` 路由与题型校验 |

## 扩展建议

- **题目来源**：若需从后端拉取题目，可在后端增加题目接口，前端在 `useQuestionBank` 中改为请求该接口，并保留 JSON 或 mock 作为兜底。
- **鉴权**：若需登录，可在 Django 增加认证与权限，前端在 `evaluation.ts` 中携带 token 或 cookie。
- **多环境**：通过环境变量或构建时注入配置后端 base URL，生产环境将 `/api` 代理到实际后端地址。
