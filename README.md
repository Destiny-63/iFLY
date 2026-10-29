# 普通话口语训练系统（iFLY）

基于讯飞 ISE 语音评测与星火大模型的普通话口语训练平台，包含 Django 后端与 Vue3 前端，支持按题型练习、录音/上传评测与 LLM 个性化反馈。

## 特色功能

- **题型专项训练**：词语、句子、篇章分页练习，题目从 JSON 配置导入，支持中英多语种展示
- **语音评测**：录音或上传 .mp3/.pcm，自动转码后调用讯飞 ISE 获取发音评分
- **LLM 反馈**：结合题目与指导重点，流式返回星火大模型的改进建议
- **题目配置**：静态 JSON 题目库，支持标题/难度/标签多语种、示范音频、收藏
- **界面**：ChatGPT 风格布局，主题与语言可配置，响应式侧栏

## 环境要求

- **后端**：Python 3.10+，ffmpeg（可选，用于 mp3 转码）
- **前端**：Node.js 18+，npm 或 pnpm
- **可选**：讯飞 ISE 与星火 API 密钥（见 [后端环境搭建](docs/backend-setup.md)）

## 快速开始

### 1. 克隆与依赖

```bash
# 后端
pip install -r requirements.txt

# 前端
cd frontend && npm install
```

### 2. 配置环境变量

在项目根目录创建 `.env`，至少配置讯飞 ISE（评测必选）；星火 API 为可选（用于 LLM 反馈）。详见 [后端环境搭建](docs/backend-setup.md)。

### 3. 启动

```bash
# 终端一：启动后端（根目录）
python manage.py runserver 0.0.0.0:8000

# 终端二：启动前端
cd frontend && npm run dev
```

浏览器访问 **http://localhost:3000**。前端通过开发代理将 `/api` 转发到后端 8000 端口。

## 文档索引

| 文档 | 说明 |
|------|------|
| [后端环境与运行](docs/backend-setup.md) | Python 环境、依赖、.env 配置、启动与常见问题 |
| [前端环境与运行](docs/frontend-setup.md) | Node 环境、依赖、启动、构建与代理说明 |
| [项目结构](docs/project-structure.md) | 前后端目录与模块说明 |
| [API 接口](docs/api.md) | 评测接口请求/响应与流式格式 |
| [前后端交互](docs/integration.md) | 请求链路、代理、流式处理与错误处理 |
| [题目导入与配置](docs/question-import.md) | JSON 题目库、多语种与字段说明 |
| [软件设计](docs/design.md) | 架构概览与模块职责 |

## 开源协议

本项目以 [MIT License](LICENSE) 开源。

## 参考链接

- [讯飞 ISE 文档](https://www.xfyun.cn/doc/Ise/IseAPI.html)
- [讯飞星火 HTTP 文档](https://www.xfyun.cn/doc/spark/X1http.html)
- [shadcn-vue](https://www.shadcn-vue.com/)
