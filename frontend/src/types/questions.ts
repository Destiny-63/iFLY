/**
 * 中英多语种配置：可为纯字符串（按中文显示）或 { zh, en } 对象
 * 题目内容、指导重点仍为中文；标题、难度、标签支持多语种展示
 */
export type I18nString = string | { zh?: string; en?: string }

/**
 * 单道题目（与 data/questions.json 结构一致，便于配置导入）
 */
export interface QuestionItem {
  /** 题目唯一标识 */
  id: string
  /** 题目标题（可选），支持多语种 */
  title?: I18nString
  /** 题目内容（必填，中文） */
  content: string
  /** 指导重点（必填，中文） */
  guidance: string
  /** 示范朗读音频 URL（可选） */
  audioExampleUrl?: string
  /** 提交评测时传给后端的 prompt，不填则用 guidance */
  prompt?: string
  /** 难度（可选），支持多语种，如 初级/Beginner */
  difficulty?: I18nString
  /** 标签（可选），支持多语种，每项可为 string 或 { zh, en } */
  tags?: (string | { zh?: string; en?: string })[]
  /** 初始/配置的练习次数（可选），与 localStorage 合并显示时以 localStorage 为准 */
  practiceCount?: number
  /** 断句信息（可选），句子/篇章专用，按意群或停顿划分的片段数组，用于前端展示断句 */
  segments?: string[]
}

/**
 * 按当前语言解析 I18nString，locale 为 'zh' | 'en' 等
 */
export function resolveI18n(value: I18nString | undefined, locale: string): string {
  if (value == null || value === '') return ''
  if (typeof value === 'string') return value
  const preferEn = locale.startsWith('en')
  return (preferEn ? value.en ?? value.zh : value.zh ?? value.en) ?? ''
}

/**
 * 解析标签数组为当前语言的字符串数组
 */
export function resolveI18nTags(tags: QuestionItem['tags'], locale: string): string[] {
  if (!tags?.length) return []
  return tags.map((t) => {
    if (typeof t === 'string') return t
    return resolveI18n(t, locale)
  }).filter(Boolean)
}

/** 按题型分组的题目库
 * character=字, word=词语, sentence=句子(可选，无专项练习时不展示), article=文章
 */
export type QuestionBank = {
  character: QuestionItem[]
  word: QuestionItem[]
  sentence: QuestionItem[]
  article: QuestionItem[]
}
