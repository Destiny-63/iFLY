# 题型专项题目配置

题目数据来自同目录下的 `questions.json`，可直接编辑该文件以配置字、词语、句子、文章各题型的题目。**支持中英多语种**：题目标题、难度、标签可配置中文与英文，界面会随用户语言切换；题目内容与指导重点仍为中文。

## 文件结构

`questions.json` 为 JSON 对象，包含四个数组，对应题型：

| 键名 | 含义 | 说明 |
|------|------|------|
| `character` | 字 | 单字练习（Character） |
| `word` | 词语 | 词语/短语练习（Word） |
| `sentence` | 句子 | 句子练习（Sentence），暂无专项练习时不展示，可留空数组 |
| `article` | 文章 | 篇章练习（Article） |

每道题目建议包含字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 题目唯一标识，如 `"character-1"`、`"word-1"`、`"article-1"` |
| `content` | 是 | 题目内容（中文，朗读/评测的文本） |
| `guidance` | 是 | 指导重点（中文，展示给用户并可作为评测提示） |
| `audioExampleUrl` | 否 | 示范朗读音频 URL，如 `"/audio/examples/xxx.mp3"` |
| `prompt` | 否 | 提交评测时传给后端的提示，不填则用 `guidance` |
| `segments` | 否 | **断句信息**（句子/篇章专用）：按意群或停顿划分的片段数组，如 `["今天", "天气", "怎么样？"]`；前端可切换「显示断句」按钮，用 `|` 分隔展示 |
| `title` | 否 | 题目标题，支持多语种（见下方） |
| `difficulty` | 否 | 难度，支持多语种，如 初级/Beginner（见下方） |
| `tags` | 否 | 标签数组，每项支持多语种（见下方） |
| `practiceCount` | 否 | 初始练习次数（未在本地存储中记录时使用，用于题目列表热力图展示） |

## 多语种配置（中英）

以下字段可写为**纯字符串**（仅中文，界面语言为英文时仍显示该字符串）或 **`{ "zh": "中文", "en": "English" }`**，界面会按当前语言显示对应文案：

- **title**：`"天气话题"` 或 `{ "zh": "天气话题", "en": "Weather Topic" }`
- **difficulty**：`"初级"` 或 `{ "zh": "初级", "en": "Beginner" }`（中级/Intermediate、高级/Advanced 同理）
- **tags**：`["声调", "轻声"]` 或 `[{ "zh": "声调", "en": "Tone" }, { "zh": "轻声", "en": "Neutral tone" }]`

缺省语言时会回退到另一种，例如只填 `zh` 时英文界面也会显示中文。

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
      "title": { "zh": "基础问候", "en": "Basic Greeting" },
      "content": "你好",
      "guidance": "请重点关注声调。",
      "difficulty": { "zh": "初级", "en": "Beginner" },
      "tags": [{ "zh": "问候", "en": "Greeting" }]
    }
  ],
  "sentence": [
    {
      "id": "sentence-1",
      "title": { "zh": "天气话题", "en": "Weather Topic" },
      "content": "今天天气怎么样？",
      "guidance": "请重点关注声调和流畅度。",
      "segments": ["今天", "天气", "怎么样？"]
    }
  ],
  "article": [
    {
      "id": "article-1",
      "title": { "zh": "春天", "en": "Spring" },
      "content": "春天来了，万物复苏。",
      "guidance": "请重点关注语流和停顿。",
      "difficulty": { "zh": "中级", "en": "Intermediate" },
      "segments": ["春天来了，", "万物复苏。"]
    }
  ]
}
```

修改保存后刷新页面即可生效（若未生效可强刷或重启前端开发服务）。
