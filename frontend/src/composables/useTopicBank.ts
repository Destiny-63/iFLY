import { ref, computed, type Ref } from 'vue'
import type { TopicBank, TopicItem } from '@/types/topics'

const TOPIC_BANK_URL = '/data/topics.json'

const cached: Ref<TopicBank | null> = ref(null)
const loading = ref(false)
const error = ref<Error | null>(null)

const fallbackTopics: TopicItem[] = [
  { id: 'topic-1', topic: '我尊敬的人', title: { zh: '我尊敬的人', en: 'A Person I Respect' }, difficulty: { zh: '初级', en: 'Beginner' }, tags: [{ zh: '人物', en: 'People' }] },
  { id: 'topic-2', topic: '我的愿望（或理想）', title: { zh: '我的愿望（或理想）', en: 'My Wish' }, difficulty: { zh: '初级', en: 'Beginner' }, tags: [{ zh: '理想', en: 'Ideal' }] },
  { id: 'topic-3', topic: '我喜欢的季节（或天气）', title: { zh: '我喜欢的季节（或天气）', en: 'My Favorite Season' }, difficulty: { zh: '初级', en: 'Beginner' }, tags: [{ zh: '自然', en: 'Nature' }] },
]

export function useTopicBank() {
  const load = async () => {
    if (cached.value !== null) return
    loading.value = true
    error.value = null
    try {
      const res = await fetch(TOPIC_BANK_URL)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      if (data?.topics && Array.isArray(data.topics)) {
        cached.value = data as TopicBank
      } else {
        throw new Error('Invalid topics.json shape')
      }
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e))
      cached.value = { topics: fallbackTopics }
    } finally {
      loading.value = false
    }
  }

  const topicBank = computed<TopicBank>(() => cached.value ?? { topics: fallbackTopics })

  const getTopics = (): TopicItem[] => topicBank.value.topics

  return {
    load,
    topicBank,
    getTopics,
    loading,
    error,
  }
}
