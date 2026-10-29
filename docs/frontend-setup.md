# 前端环境搭建与运行

本文说明 Vue3 前端的依赖、启动、构建及与后端的代理配置。

## 环境要求

- Node.js 18+
- npm、pnpm 或 yarn 任选其一

## 安装步骤

### 1. 进入前端目录

```bash
cd frontend
```

### 2. 安装依赖

```bash
npm install
# 或
pnpm install
```

### 3. 启动开发服务器

```bash
npm run dev
```

前端默认运行在 **http://localhost:3000**。请同时启动后端（见 [后端环境与运行](backend-setup.md)），否则评测等接口会失败。

## 代理配置

开发环境下，Vite 将前端的 `/api` 请求代理到后端：

- 前端：`http://localhost:3000`
- 代理：`/api` → `http://127.0.0.1:8000`

因此前端请求 `fetch('/api/evaluation/')` 会发往 `http://127.0.0.1:8000/api/evaluation/`，无需单独配置 CORS。

配置见 `frontend/vite.config.ts`：

```ts
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    },
  },
}
```

## 构建与预览

```bash
# 生产构建
npm run build

# 本地预览构建结果（需自行解决 /api 代理或直连后端）
npm run preview
```

生产部署时需将静态资源部署到 Web 服务器，并将 `/api` 反向代理到 Django 后端。

## 常见问题

1. **录音不可用**：需 HTTPS 或 localhost，并授予麦克风权限；部分浏览器需 MediaRecorder 支持。
2. **接口 404/502**：确认后端已启动在 8000 端口，且 Vite 代理配置正确。
3. **题目不显示**：检查 `frontend/public/data/questions.json` 是否存在且格式正确，见 [题目导入与配置](question-import.md)。
