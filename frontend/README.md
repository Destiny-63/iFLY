# 普通话口语训练前端

基于 Vue3 + shadcn-vue 的题型专项练习与评测前端，通过 `/api` 代理与 Django 后端通信。

## 功能概览

- 题型专项：词语 / 句子 / 篇章分页，题目来自 `public/data/questions.json`，支持多语种与收藏
- 题目展示：标题、难度、标签、示范音频、指导重点输入
- 评测：录音或上传 .mp3/.pcm，提交后流式展示 ISE 评分与 LLM 反馈
- 界面：侧栏、主题与语言可配置

## 快速开始

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000。需同时启动后端（见项目根目录 [README.md](../README.md) 与 [docs/backend-setup.md](../docs/backend-setup.md)）。

## 文档

- **环境与运行**：[docs/frontend-setup.md](../docs/frontend-setup.md)
- **项目结构**：[docs/project-structure.md](../docs/project-structure.md)
- **题目配置**：[public/data/README.md](public/data/README.md)，题目导入总览见 [docs/question-import.md](../docs/question-import.md)
