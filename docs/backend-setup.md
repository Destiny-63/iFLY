# 后端环境搭建与运行

本文说明 Django 后端的依赖、环境变量、启动方式及常见问题。

## 环境要求

- Python 3.10 或以上
- ffmpeg（可选）：用于将 .mp3 转为 16kHz/16bit 单声道 PCM；未安装时请直接使用 .pcm 或由前端/其他方式转码

## 安装步骤

### 1. 创建虚拟环境（推荐）

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

### 2. 安装依赖

在项目根目录执行：

```bash
pip install -r requirements.txt
```

### 3. 环境变量

在项目根目录创建 `.env` 文件：

```env
# Django
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=*

# 讯飞 ISE（语音评测，必填）
APP_ID=your_ise_app_id
API_KEY=your_ise_api_key
API_SECRET=your_ise_api_secret

# 星火大模型（LLM 反馈，可选；不配置则只返回 ISE 评测结果）
SPARK_API_KEY=your_spark_api_key
SPARK_API_URL=https://spark-api-open.xf-yun.com/v1
SPARK_MODEL=generalv3.5
```

- **ISE**：在 [讯飞开放平台](https://www.xfyun.cn/) 创建应用并开通「语音评测」服务，将控制台中的 APP_ID、API_KEY、API_SECRET 填入。
- **星火**：在控制台开通星火服务，获取 API 密钥；`SPARK_API_URL` 与 `SPARK_MODEL` 按所购版本填写（如 v2、x2 等），详见平台文档。

## 运行

```bash
# 项目根目录
python manage.py runserver 0.0.0.0:8000
```

服务默认在 **http://127.0.0.1:8000**。生产部署请使用 gunicorn/uwsgi 并关闭 DEBUG。

## API 文档

启动后可访问自动生成的接口文档：

- Swagger UI：http://127.0.0.1:8000/api/docs/
- ReDoc：http://127.0.0.1:8000/api/redoc/
- OpenAPI Schema：http://127.0.0.1:8000/api/schema/

导出 Schema：

```bash
python manage.py spectacular --file schema.yml
python manage.py spectacular --file schema.json
```

## 常见问题

1. **mp3 转换失败**：安装 ffmpeg 并加入 PATH，或改为上传 .pcm 文件。
2. **ISE 鉴权失败**：检查 .env 中 APP_ID、API_KEY、API_SECRET 是否正确，应用是否已开通语音评测。
3. **无 LLM 反馈**：确认已配置 SPARK_API_KEY、SPARK_API_URL，且星火服务已开通；未配置时仅返回 ISE 评测结果。
4. **CORS 报错**：开发环境下前端通过 Vite 代理访问 `/api`，一般不涉及跨域；若直连后端，需在 Django 中配置 CORS 白名单。
