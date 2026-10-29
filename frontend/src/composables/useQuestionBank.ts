import { ref, computed, type Ref } from 'vue'
import type { QuestionBank, QuestionItem } from '@/types/questions'
import { fallbackQuestionBank } from '@/data/mock'

const QUESTION_BANK_URL = '/data/questions.json'

const cached: Ref<QuestionBank | null> = ref(null)
const loading = ref(false)
const error = ref<Error | null>(null)

/**
 * 从静态 JSON 加载题型专项题目库，失败时使用 mock 中的默认数据。
 * 题目库放在 frontend/public/data/questions.json，可直接编辑配置。
 */
export function useQuestionBank() {
  const load = async () => {
    if (cached.value !== null) return
    loading.value = true
    error.value = null
    try {
      const res = await fetch(QUESTION_BANK_URL)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      if (data && typeof data === 'object' && Array.isArray(data.character) && Array.isArray(data.word) && Array.isArray(data.sentence) && Array.isArray(data.article)) {
        cached.value = data as QuestionBank
      } else {
        throw new Error('Invalid questions.json shape')
      }
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e))
      cached.value = fallbackQuestionBank
    } finally {
      loading.value = false
    }
  }

  const questionBank = computed<QuestionBank>(() => cached.value ?? fallbackQuestionBank)

  /** 按题型取题目列表，character=字 word=词语 sentence=句子 article=文章 */
  const getQuestionsByType = (type: 'character' | 'word' | 'sentence' | 'article'): QuestionItem[] => {
    return questionBank.value[type] ?? []
  }

  return {
    load,
    questionBank,
    getQuestionsByType,
    loading,
    error,
  }
}
