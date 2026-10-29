import type { I18nString } from './questions'

export interface TopicItem {
  id: string
  topic: string
  title?: I18nString
  /** 难度，如 初级/Beginner */
  difficulty?: I18nString
  /** 标签，如 人物、理想 */
  tags?: (string | { zh?: string; en?: string })[]
}

export interface TopicBank {
  topics: TopicItem[]
}
