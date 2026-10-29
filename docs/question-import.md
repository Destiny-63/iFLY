# 题目导入与配置

题型专项的题目来自前端静态 JSON 文件，无需后端参与。支持按题型配置、多语种展示和示范音频。

## 题目文件位置

- **路径**：`frontend/public/data/questions.json`
- **说明**：修改该文件后刷新页面即可生效（开发时热更新可能不会重载 public，可强刷或重启前端）。

## 文件结构

根对象包含四个数组，对应四种题型：

| 键名 | 含义 | 说明 |
|------|------|------|
| `character` | 字 | 单字练习（Character） |
| `word` | 词语 | 词语/短语练习（Word） |
| `sentence` | 句子 | 句子练习（Sentence），暂无专项练习时不展示，可留空数组 |
| `article` | 文章 | 篇章练习（Article） |

每道题目为对象，字段说明如下。

### 必填字段

| 字段 | 说明 |
|------|------|
| `id` | 题目唯一标识，如 `"character-1"`、`"word-1"`、`"article-1"` |
| `content` | 题目内容（中文），即朗读/评测的文本 |
| `guidance` | 指导重点（中文），展示在输入框并可作为默认提交内容 |

### 可选字段

| 字段 | 说明 |
|------|------|
| `title` | 题目标题，支持多语种（见下） |
| `difficulty` | 难度，如「初级」「中级」，支持多语种 |
| `tags` | 标签数组，每项可为字符串或多语种对象 |
| `audioExampleUrl` | 示范朗读音频 URL，如 `"/audio/examples/xxx.mp3"` |
| `prompt` | 提交评测时若用户未修改输入框，则使用该值作为 `guidance` 发给后端；不填则用 `guidance` |
| `practiceCount` | 初始练习次数：该题在本机尚未有记录时，用于题目列表热力图展示；用户练习后以本地存储为准 |
| `segments` | **断句信息**（句子/篇章专用）：按意群或停顿划分的片段数组，如 `["今天", "天气", "怎么样？"]`；前端可切换「显示断句」按钮，用 `|` 分隔展示 |

### 多语种（中英）

以下字段可写为**纯字符串**（仅中文）或 **`{ "zh": "中文", "en": "English" }`**，界面会按当前语言显示：

- **title**：题目标题
- **difficulty**：难度（如 初级/Beginner、中级/Intermediate）
- **tags**：标签，每项可为 `"声调"` 或 `{ "zh": "声调", "en": "Tone" }`

缺省语言时会回退到另一种（例如只填 `zh` 时英文界面也显示中文）。

## 示例

```json
{
  "character": [
    {
      "id": "character-1",
      "title": { "zh": "单字声调", "en": "Character Tones" },
      "content": "你",
      "guidance": "请重点关注声调。",
      "difficulty": { "zh": "初级", "en": "Beginner" },
      "tags": [{ "zh": "声调", "en": "Tone" }]
    }
  ],
  "word": [
    {
      "id": "word-1",
      "title": { "zh": "天气话题", "en": "Weather Topic" },
      "content": "今天天气怎么样",
      "guidance": "请重点关注声调和流畅度。",
      "audioExampleUrl": "/audio/examples/read_sentence_cn.mp3",
      "prompt": "请重点关注声调和流畅度",
      "difficulty": { "zh": "初级", "en": "Beginner" },
      "tags": [{ "zh": "日常", "en": "Daily" }, { "zh": "语调", "en": "Intonation" }],
      "practiceCount": 0
    }
  ],
  "sentence": [
    {
      "id": "sentence-1",
      "title": { "zh": "天气话题", "en": "Weather Topic" },
      "content": "今天天气怎么样？",
      "guidance": "请重点关注声调和流畅度。",
      "audioExampleUrl": "/audio/examples/read_sentence_cn.mp3",
      "difficulty": { "zh": "初级", "en": "Beginner" },
      "tags": [{ "zh": "日常", "en": "Daily" }],
      "segments": ["今天", "天气", "怎么样？"]
    }
  ],
  "article": [
    {
      "id": "article-1",
      "title": { "zh": "春天", "en": "Spring" },
      "content": "春天来了，万物复苏，大地一片生机勃勃的景象。",
      "guidance": "请重点关注语流和停顿。",
      "difficulty": { "zh": "中级", "en": "Intermediate" },
      "segments": ["春天来了，", "万物复苏，", "大地一片生机勃勃的景象。"]
    }
  ]
}
```

## 加载与兜底

- 前端通过 `fetch('/data/questions.json')` 加载题目；若请求失败或格式错误，会使用 `src/data/mock.ts` 中的 `fallbackQuestionBank`，保证页面仍有题目可做。
- 题目展示、难度与标签的解析逻辑见 `src/types/questions.ts`（`resolveI18n`、`resolveI18nTags`）。

更细的字段说明与多语种示例见 **`frontend/public/data/README.md`**。
