import axios from 'axios'

export interface EvaluationResult {
  total_score: number
  accuracy_score: number
  fluency_score: number
  integrity_score: number
  tone_score?: number
  phone_score?: number
  raw_xml?: string
}

export interface StreamChunk {
  type: 'evaluation' | 'feedback_chunk' | 'done' | 'error' | 'info'
  data?: EvaluationResult | string
  detail?: string
}

export async function submitEvaluation(
  audioFile: File,
  questionText: string,
  guidance: string,
  onChunk: (chunk: StreamChunk) => void
): Promise<void> {
  const formData = new FormData()
  formData.append('audio', audioFile)
  formData.append('question_text', questionText)
  formData.append('guidance', guidance)

  let response: Response
  try {
    response = await fetch('/api/evaluation/', {
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
        const error = JSON.parse(text)
        errMsg = error.detail || `请求失败 (${status})`
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
          const chunk: StreamChunk = JSON.parse(line)
          onChunk(chunk)
        } catch (e) {
          console.error('解析 JSON 失败:', line, e)
        }
      }
    }
  }

  // 处理剩余的 buffer
  if (buffer.trim()) {
    try {
      const chunk: StreamChunk = JSON.parse(buffer)
      onChunk(chunk)
    } catch (e) {
      console.error('解析 JSON 失败:', buffer, e)
    }
  }
}
