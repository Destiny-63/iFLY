import { ref } from 'vue'

export function useAudioRecorder() {
  const TARGET_SAMPLE_RATE = 16000
  const isRecording = ref(false)
  const audioBlob = ref<Blob | null>(null)
  const audioUrl = ref<string | null>(null)
  let mediaRecorder: MediaRecorder | null = null
  let audioChunks: Blob[] = []

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus',
      })

      audioChunks = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data)
        }
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunks, { type: 'audio/webm' })
        audioBlob.value = blob
        audioUrl.value = URL.createObjectURL(blob)
        stream.getTracks().forEach((track) => track.stop())
      }

      mediaRecorder.start()
      isRecording.value = true
    } catch (error) {
      console.error('录音失败:', error)
      throw error
    }
  }

  const stopRecording = () => {
    if (mediaRecorder && isRecording.value) {
      mediaRecorder.stop()
      isRecording.value = false
    }
  }

  const resampleTo16kMono = (audioBuffer: AudioBuffer): Float32Array => {
    const sourceRate = audioBuffer.sampleRate
    const channelCount = audioBuffer.numberOfChannels
    const sourceLength = audioBuffer.length

    const mixed = new Float32Array(sourceLength)
    for (let i = 0; i < sourceLength; i++) {
      let sum = 0
      for (let ch = 0; ch < channelCount; ch++) {
        sum += audioBuffer.getChannelData(ch)[i]
      }
      mixed[i] = sum / channelCount
    }

    if (sourceRate === TARGET_SAMPLE_RATE) {
      return mixed
    }

    const ratio = sourceRate / TARGET_SAMPLE_RATE
    const targetLength = Math.round(sourceLength / ratio)
    const result = new Float32Array(targetLength)
    for (let i = 0; i < targetLength; i++) {
      const sourceIndex = i * ratio
      const left = Math.floor(sourceIndex)
      const right = Math.min(left + 1, sourceLength - 1)
      const weight = sourceIndex - left
      result[i] = mixed[left] * (1 - weight) + mixed[right] * weight
    }
    return result
  }

  const floatTo16BitPCM = (samples: Float32Array): ArrayBuffer => {
    const buffer = new ArrayBuffer(samples.length * 2)
    const view = new DataView(buffer)
    for (let i = 0; i < samples.length; i++) {
      const sample = Math.max(-1, Math.min(1, samples[i]))
      const value = sample < 0 ? sample * 0x8000 : sample * 0x7fff
      view.setInt16(i * 2, value, true)
    }
    return buffer
  }

  const convertToPCM = async (blob: Blob): Promise<Blob> => {
    const audioContext = new AudioContext()
    try {
      const input = await blob.arrayBuffer()
      const audioBuffer = await audioContext.decodeAudioData(input.slice(0))
      const mono16k = resampleTo16kMono(audioBuffer)
      const pcmBuffer = floatTo16BitPCM(mono16k)
      return new Blob([pcmBuffer], { type: 'audio/pcm' })
    } finally {
      await audioContext.close()
    }
  }

  const getAudioFile = async (): Promise<File | null> => {
    if (!audioBlob.value) return null
    const pcmBlob = await convertToPCM(audioBlob.value)
    return new File([pcmBlob], 'recording.pcm', { type: 'audio/pcm' })
  }

  const reset = () => {
    if (audioUrl.value) {
      URL.revokeObjectURL(audioUrl.value)
    }
    audioBlob.value = null
    audioUrl.value = null
    audioChunks = []
  }

  return {
    isRecording,
    audioBlob,
    audioUrl,
    startRecording,
    stopRecording,
    getAudioFile,
    reset,
  }
}
