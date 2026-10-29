# 项目结构

本文描述前后端目录与主要模块的职责。

## 仓库根目录

```
iFLY/
├── README.md                 # 项目介绍、快速开始、文档索引
├── requirements.txt          # Python 依赖
├── manage.py                 # Django 入口
├── .env                      # 环境变量（需自行创建，不提交）
├── config/                   # Django 配置
│   └── settings.py
├── apps/                     # Django 应用
│   └── evaluation/           # 评测接口与业务
├── services/                 # 外部服务封装
│   ├── ise_service.py        # 讯飞 ISE 评测
│   ├── spark_service.py      # 星火大模型
│   └── audio_processor.py    # 音频格式处理（mp3 → pcm）
├── frontend/                 # Vue3 前端
└── docs/                     # 项目文档
```

## 后端（Django）

| 路径 | 说明 |
|------|------|
| `config/` | 项目配置、路由、WSGI/ASGI |
| `apps/evaluation/` | 评测应用：视图、序列化、URL、测试 |
| `apps/evaluation/views.py` | 评测 API 视图，处理上传与流式响应 |
| `apps/evaluation/serializers.py` | 请求参数校验 |
| `services/ise_service.py` | 调用讯飞 ISE 评测 |
| `services/spark_service.py` | 调用星火流式生成反馈 |
| `services/audio_processor.py` | mp3 转 16kHz/16bit 单声道 PCM |

## 前端（Vue3）

```
frontend/
├── public/
│   ├── data/
│   │   ├── questions.json    # 题目库（词语/句子/篇章）
│   │   └── README.md         # 题目配置说明
│   └── audio/                # 静态音频资源（如示范音频）
├── src/
│   ├── api/                  # 接口封装
│   │   └── evaluation.ts     # 评测接口（流式）
│   ├── components/           # 组件
│   │   ├── ui/               # shadcn-vue 基础组件
│   │   ├── Sidebar.vue       # 侧栏与题型导航
│   │   ├── EvaluationResult.vue
│   │   └── GuidanceRichText.vue
│   ├── composables/         # 组合式函数
│   │   ├── useQuestionBank.ts  # 题目库加载（JSON）
│   │   ├── useAudioRecorder.ts # 录音
│   │   └── useSettings.ts      # 主题/语言等
│   ├── data/
│   │   └── mock.ts           # 默认题目与侧栏数据（fallback）
│   ├── types/
│   │   └── questions.ts      # 题目类型与多语种解析
│   ├── views/
│   │   └── Home.vue          # 主页面（题型练习 + 评测 + 反馈）
│   ├── router/
│   │   └── index.ts          # 路由（/question-type/:type）
│   ├── locales/              # 中英文案
│   └── style.css
├── vite.config.ts            # Vite 配置与 /api 代理
└── package.json
```

路由约定：

- `/` 重定向到 `/question-type/sentence`
- `/question-type/word|sentence|passage` 对应词语/句子/篇章题型页
