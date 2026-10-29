/** PSC 命题说话 40 分制评分（LLM 输出） */
export interface PscScore {
  dim1_deduct?: number
  dim2_deduct?: number
  dim3_deduct?: number
  total?: number
}

export interface TopicSpeakingResult {
  topic: string
  duration_seconds: number
  transcript: string
  ise_result: {
    total_score?: number
    accuracy_score?: number
    fluency_score?: number
    integrity_score?: number
    tone_score?: number
    phone_score?: number
  } | null
  time_penalty: {
    deduct: number
    reason: string
    shortfall_seconds: number
  }
  /** PSC 40 分制总分与各维度扣分（LLM 解析后追加） */
  psc_score?: PscScore
}

export interface TopicStreamChunk {
  type: 'evaluation' | 'evaluation_update' | 'feedback_chunk' | 'done' | 'error' | 'info'
  data?: TopicSpeakingResult | string | { psc_score?: PscScore }
  detail?: string
}

export async function submitTopicSpeaking(
  audioFile: File,
  topic: string,
  onChunk: (chunk: TopicStreamChunk) => void
): Promise<void> {
  const formData = new FormData()
  formData.append('audio', audioFile)
  formData.append('topic', topic)

  let response: Response
  try {
    response = await fetch('/api/topic-speaking/', {
      method: 'POST',
      body: formData,
    })
  } catch (e) {
    const orig = e instanceof Error ? e.message : String(e)
    throw new Error(`网络连接失败，请检查后端是否已启动: ${orig}`)
  }

  if (!response.ok) {
    const status = response.status
    let errMsg: string
    try {
      const text = await response.text()
      if (text.trim()) {
        const err = JSON.parse(text)
        errMsg = err.detail || `请求失败 (${status})`
      } else if (status >= 500) {
        errMsg = `服务器返回异常状态 ${status} 且无有效响应体，可能是后端未启动或崩溃`
      } else {
        errMsg = `请求被拒绝 (${status})`
      }
    } catch (parseErr) {
      errMsg = status >= 500
        ? `服务器返回异常状态 ${status}，但响应格式无法解析，可能是代理错误页或后端异常`
        : `请求被拒绝 (${status})`
    }
    throw new Error(errMsg)
  }

  const reader = response.body?.getReader()
  const decoder = new TextDecoder()

  if (!reader) {
    throw new Error('无法读取响应流，可能是连接已断开或服务异常')
  }

  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''

    for (const line of lines) {
      if (line.trim()) {
        try {
          const chunk: TopicStreamChunk = JSON.parse(line)
          onChunk(chunk)
        } catch (e) {
          console.error('解析 JSON 失败:', line, e)
        }
      }
    }
  }

  if (buffer.trim()) {
    try {
      const chunk: TopicStreamChunk = JSON.parse(buffer)
      onChunk(chunk)
    } catch (e) {
      console.error('解析 JSON 失败:', buffer, e)
    }
  }
}
