<template>
  <SidebarProvider>
    <Sidebar />

    <!-- 主内容区 -->
    <SidebarInset>
      <header class="flex h-14 items-center gap-2 border-b bg-card px-4">
        <SidebarTrigger />
        <div class="text-sm text-muted-foreground">{{ $t('home.questionTypeSection') }} / {{ $t(`sidebar.${currentType}`) }}</div>
      </header>
      <div class="flex min-h-0 flex-1 flex-col">
      <!-- 题目区域 -->
      <div class="border-b bg-card p-4">
        <template v-if="questionsByType.length">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <h2 class="flex items-baseline gap-1.5">
                <span class="text-sm font-medium text-muted-foreground">{{ $t('home.question') }}</span>
                <span class="text-3xl font-semibold tabular-nums">{{ currentQuestionIndex + 1 }}</span>
                <span class="text-sm text-muted-foreground">/ {{ questionsByType.length }}</span>
              </h2>
              <Badge variant="outline">{{ currentType === 'character' ? $t('sidebar.character') : currentType === 'word' ? $t('sidebar.word') : currentType === 'sentence' ? $t('sidebar.sentence') : $t('sidebar.article') }}</Badge>
            </div>
            <div class="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                class="h-9 w-9 shrink-0 p-0"
                :disabled="currentQuestionIndex === 0"
                :aria-label="$t('home.previous')"
                @click="previousQuestion"
              >
                <ChevronLeft class="size-4" />
              </Button>
              <Button
                variant="outline"
                size="sm"
                class="h-9 w-9 shrink-0 p-0"
                :disabled="currentQuestionIndex === questionsByType.length - 1"
                :aria-label="$t('home.next')"
                @click="nextQuestion"
              >
                <ChevronRight class="size-4" />
              </Button>
              <Button
                variant="outline"
                size="sm"
                class="h-9 w-9 shrink-0 p-0"
                :aria-label="$t('home.questionList')"
                @click="questionSheetOpen = true"
              >
                <LayoutGrid class="size-4" />
              </Button>
            </div>
          </div>

          <!-- 题目列表 / 练习热力图 Sheet（右侧滑出） -->
          <Sheet v-model:open="questionSheetOpen">
            <SheetContent side="right" class="w-full sm:max-w-md">
              <SheetHeader>
                <SheetTitle>{{ $t('home.questionList') }}</SheetTitle>
                <SheetDescription>{{ $t('home.questionListDesc') }}</SheetDescription>
              </SheetHeader>
              <div class="mt-4">
                <p class="mb-2 text-xs text-muted-foreground">{{ $t('home.practiceHeatmapLegend') }}</p>
                <div class="flex flex-wrap gap-2">
                  <span class="inline-flex items-center gap-1 rounded border px-2 py-0.5 text-xs">
                    <span class="size-3 rounded-sm bg-muted" /> {{ $t('home.notPracticed') }}
                  </span>
                  <span class="inline-flex items-center gap-1 rounded border px-2 py-0.5 text-xs">
                    <span class="size-3 rounded-sm bg-primary/30" /> 1+
                  </span>
                  <span class="inline-flex items-center gap-1 rounded border px-2 py-0.5 text-xs">
                    <span class="size-3 rounded-sm bg-primary/60" /> 3+
                  </span>
                </div>
                <div class="mt-4 grid grid-cols-5 gap-3 sm:grid-cols-6">
                  <button
                    v-for="(q, idx) in questionsByType"
                    :key="q.id"
                    type="button"
                    class="flex size-10 min-w-0 items-center justify-center rounded-md text-base font-semibold tabular-nums transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                    :class="getQuestionCellClass(q, idx)"
                    :title="`${q.content?.slice(0, 20)}${(q.content?.length ?? 0) > 20 ? '…' : ''} · ${$t('home.practiceCount')}: ${getPracticeCount(q)}`"
                    @click="goToQuestion(idx)"
                  >
                    {{ idx + 1 }}
                  </button>
                </div>
              </div>
            </SheetContent>
          </Sheet>
          <div class="mt-4">
            <Card>
              <CardContent class="p-6 space-y-4">
                <!-- 标题行：左侧标题，右侧难度+标签+收藏 -->
                <div class="flex flex-wrap items-center justify-between gap-2">
                  <p v-if="resolvedTitle" class="flex items-center gap-1.5 text-sm font-medium text-muted-foreground">
                    <BookOpen class="size-4 shrink-0" />
                    {{ resolvedTitle }}
                  </p>
                  <div class="flex flex-wrap items-center gap-2 sm:gap-3">
                    <!-- 难度标签已隐藏
                    <span v-if="resolvedDifficulty" class="flex items-center gap-1.5 rounded-md bg-primary/15 px-2 py-1 text-xs font-medium text-primary">
                      <Gauge class="size-4 shrink-0" />
                      {{ resolvedDifficulty }}
                    </span>
                    -->
                    <span v-if="resolvedTags.length" class="flex items-center gap-1.5 text-sm text-muted-foreground">
                      <Tag class="size-4 shrink-0" />
                      <span class="flex flex-wrap gap-1">
                        <span
                          v-for="tag in resolvedTags"
                          :key="tag"
                          class="rounded-md border bg-background px-2 py-0.5 text-xs"
                        >
                          {{ tag }}
                        </span>
                      </span>
                    </span>
                    <Button
                      v-if="currentQuestion?.segments?.length"
                      variant="outline"
                      size="sm"
                      class="h-8 shrink-0"
                      :aria-label="showSegments ? $t('home.hideSegments') : $t('home.showSegments')"
                      @click="showSegments = !showSegments"
                    >
                      <SeparatorHorizontal class="mr-1 size-4" />
                      {{ showSegments ? $t('home.hideSegments') : $t('home.showSegments') }}
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      class="h-8 w-8 shrink-0"
                      :class="isFavorite(currentQuestion?.id) ? 'text-primary' : 'text-muted-foreground'"
                      :aria-label="isFavorite(currentQuestion?.id) ? $t('home.unfavorite') : $t('home.favorite')"
                      @click="toggleFavorite(currentQuestion?.id)"
                    >
                      <Star
                        class="size-4"
                        :class="{ 'fill-current': isFavorite(currentQuestion?.id) }"
                      />
                    </Button>
                  </div>
                </div>
                <!-- 正文 -->
                <p class="text-lg">
                  <template v-if="showSegments && currentQuestion?.segments?.length">
                    <span
                      v-for="(seg, i) in currentQuestion.segments"
                      :key="i"
                    >
                      {{ seg }}<span v-if="i < (currentQuestion?.segments?.length ?? 0) - 1" class="mx-1 text-muted-foreground/70">|</span>
                    </span>
                  </template>
                  <template v-else>
                    {{ currentQuestion?.content }}
                  </template>
                </p>
                <!-- 题目音频示例（有配置时显示） -->
                <div v-if="currentQuestion?.audioExampleUrl" class="flex flex-wrap items-center gap-3">
                  <span class="flex shrink-0 items-center gap-1.5 text-sm text-muted-foreground">
                    <Mic class="size-4" />
                    {{ $t('home.audioExample') }}
                  </span>
                  <audio
                    :src="currentQuestion.audioExampleUrl"
                    controls
                    class="audio-theme h-9 min-w-0 flex-1 max-w-md"
                  />
                </div>
                <!-- 指导重点 -->
                <div class="space-y-2">
                  <span class="flex items-center gap-1.5 text-sm text-muted-foreground">
                    <Target class="size-4" />
                    {{ $t('home.guidanceFocus') }}
                  </span>
                  <Input
                    v-model="guidanceInput"
                    :placeholder="$t('home.guidancePlaceholder')"
                  />
                </div>
              </CardContent>
            </Card>
          </div>
        </template>
        <div v-else class="rounded-xl border border-dashed bg-muted/30 p-8 text-center text-muted-foreground">
          {{ $t('home.noQuestions') }}
        </div>
      </div>

      <!-- 聊天区域 -->
      <ScrollArea class="flex-1">
        <div class="space-y-4 p-4">
          <!-- 评测结果 -->
          <EvaluationResult v-if="evaluationResult" :result="evaluationResult" />

          <!-- LLM 指导意见历史 -->
          <div v-for="(message, index) in messages" :key="index">
            <GuidanceRichText :content="message.content" :timestamp="message.timestamp" />
          </div>

          <!-- Loading -->
          <div v-if="isLoading" class="flex items-center justify-center gap-2 p-4">
            <Spinner />
            <span class="text-sm text-muted-foreground">{{ $t('home.evaluating') }}</span>
          </div>

          <!-- 流式输出中的反馈 -->
          <div v-if="streamingFeedback">
            <GuidanceRichText :content="streamingFeedback" />
          </div>
        </div>
      </ScrollArea>

      <!-- 输入区域：单输入器（文本/录音互斥） -->
      <div class="border-t bg-card p-4">
        <div
          class="rounded-3xl border bg-background p-3 shadow-sm transition-colors"
          :class="isDragOver ? 'border-primary bg-primary/5' : ''"
          @dragenter.prevent="isDragOver = true"
          @dragover.prevent="isDragOver = true"
          @dragleave.prevent="isDragOver = false"
          @drop.prevent="onDropAudio"
        >
          <input
            ref="fileInputRef"
            type="file"
            accept=".pcm,.mp3,audio/mpeg,audio/pcm"
            class="hidden"
            @change="onFileSelected"
          />

          <!-- 上传文件和录音展示区域（放在上方） -->
          <div v-if="uploadedAudioFile || audioUrl" class="mb-2 space-y-2">
            <div v-if="uploadedAudioFile" class="flex items-center gap-2 rounded-md bg-muted/50 px-2 py-1.5">
              <span class="text-xs text-muted-foreground flex-1 truncate">
                {{ $t('home.uploaded') }}{{ uploadedAudioFile.name }}
              </span>
              <Button variant="ghost" size="sm" class="h-6 px-2 text-xs" @click="clearUploadedFile">{{ $t('home.clear') }}</Button>
            </div>
            <div v-if="audioUrl" class="flex items-center gap-2 rounded-md bg-muted/50 px-2 py-1.5">
              <span class="text-xs text-muted-foreground">{{ $t('home.recordingReady') }}</span>
              <audio :src="audioUrl" controls class="h-6 flex-1"></audio>
              <Button variant="ghost" size="sm" class="h-6 px-2 text-xs" @click="clearRecordedAudio">{{ $t('home.clear') }}</Button>
            </div>
          </div>

          <Textarea
            v-model="textInput"
            :disabled="isLoading"
            :placeholder="$t('home.inputPlaceholder')"
            class="min-h-[72px] resize-none border-0 p-1 text-base shadow-none focus-visible:ring-0"
            @keydown.enter.exact.prevent="submitCombined"
          />

          <div class="mt-2 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <Button variant="ghost" size="icon" class="rounded-full" :disabled="isLoading || isRecording" @click="openFilePicker">
                <Plus class="size-5" />
              </Button>
              <div class="flex items-center gap-1">
                <Button
                  size="sm"
                  class="h-7 rounded-full px-2 text-xs"
                  :variant="audioSource === 'record' ? 'default' : 'ghost'"
                  :disabled="!audioBlob"
                  @click="audioSource = 'record'"
                >
                  {{ $t('home.record') }}
                </Button>
                <Button
                  size="sm"
                  class="h-7 rounded-full px-2 text-xs"
                  :variant="audioSource === 'upload' ? 'default' : 'ghost'"
                  :disabled="!uploadedAudioFile"
                  @click="audioSource = 'upload'"
                >
                  {{ $t('home.upload') }}
                </Button>
              </div>
              <span class="text-xs text-muted-foreground">{{ $t('home.dragDropHint') }}</span>
            </div>

            <div class="flex items-center gap-2">
              <Button
                :variant="isRecording ? 'destructive' : 'default'"
                size="icon"
                class="rounded-full"
                :disabled="isLoading"
                @click="toggleRecording"
              >
                <Mic class="size-5" />
              </Button>
              <Button
                size="icon"
                class="rounded-full"
                variant="default"
                :disabled="isLoading || isRecording || !hasSelectedAudio || !questionsByType.length"
                @click="submitCombined"
              >
                <SendHorizontal class="size-5" />
              </Button>
            </div>
          </div>
        </div>
      </div>
      </div>
    </SidebarInset>

    <!-- 错误提示弹窗 -->
    <Dialog v-model:open="errorDialogOpen">
      <DialogContent class="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{{ $t('topicSpeaking.errorTitle') }}</DialogTitle>
          <DialogDescription>{{ errorMessage }}</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button @click="errorDialogOpen = false">{{ $t('topicSpeaking.errorConfirm') }}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </SidebarProvider>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import EvaluationResult from '@/components/EvaluationResult.vue'
import GuidanceRichText from '@/components/GuidanceRichText.vue'
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Spinner } from '@/components/ui/spinner'
import { BookOpen, ChevronLeft, ChevronRight, Gauge, LayoutGrid, Mic, Plus, SendHorizontal, SeparatorHorizontal, Star, Tag, Target } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { useQuestionBank } from '@/composables/useQuestionBank'
import { submitEvaluation, type EvaluationResult as EvalResult } from '@/api/evaluation'
import { useAudioRecorder } from '@/composables/useAudioRecorder'
import { useSettings } from '@/composables/useSettings'
import { resolveI18n, resolveI18nTags } from '@/types/questions'

useSettings()

const { locale } = useI18n()
const route = useRoute()
const currentType = computed(() => {
  const t = route.params.type as string
  return t === 'character' || t === 'word' || t === 'sentence' || t === 'article' ? t : 'word'
})

const { getQuestionsByType, load } = useQuestionBank()
onMounted(() => load())

const questionsByType = computed(() => getQuestionsByType(currentType.value as 'character' | 'word' | 'sentence' | 'article'))
const currentQuestionIndex = ref(0)
const currentQuestion = computed(() => questionsByType.value[currentQuestionIndex.value])

const resolvedTitle = computed(() => resolveI18n(currentQuestion.value?.title, locale.value))
const resolvedDifficulty = computed(() => resolveI18n(currentQuestion.value?.difficulty, locale.value))
const resolvedTags = computed(() => resolveI18nTags(currentQuestion.value?.tags, locale.value))

const FAVORITE_STORAGE_KEY = 'ifly-question-favorites'
const favoriteIds = ref<Set<string>>(new Set(JSON.parse(localStorage.getItem(FAVORITE_STORAGE_KEY) ?? '[]')))

const PRACTICE_COUNT_KEY = 'ifly-question-practice-count'
const practiceCounts = ref<Record<string, number>>(
  (() => {
    try {
      return JSON.parse(localStorage.getItem(PRACTICE_COUNT_KEY) ?? '{}')
    } catch {
      return {}
    }
  })()
)
const getPracticeCount = (q: { id: string; practiceCount?: number } | undefined) => {
  if (!q) return 0
  return practiceCounts.value[q.id] ?? q.practiceCount ?? 0
}
const incrementPracticeCount = (id: string | undefined) => {
  if (!id) return
  const next = { ...practiceCounts.value, [id]: (practiceCounts.value[id] ?? 0) + 1 }
  practiceCounts.value = next
  localStorage.setItem(PRACTICE_COUNT_KEY, JSON.stringify(next))
}
const getQuestionCellClass = (q: { id: string; practiceCount?: number } | undefined, idx: number) => {
  if (!q) return ''
  const count = getPracticeCount(q)
  const isCurrent = idx === currentQuestionIndex.value
  const base = 'hover:opacity-90'
  if (isCurrent) return `bg-primary text-primary-foreground shadow-sm ${base}`
  if (count === 0) return `bg-muted text-muted-foreground hover:bg-muted/80 ${base}`
  if (count >= 3) return `bg-primary/70 text-primary-foreground ${base}`
  return `bg-primary/40 text-primary-foreground ${base}`
}
const questionSheetOpen = ref(false)
const showSegments = ref(false)
const errorDialogOpen = ref(false)
const errorMessage = ref('')
const showError = (msg: string) => {
  errorMessage.value = msg
  errorDialogOpen.value = true
}
const goToQuestion = (idx: number) => {
  currentQuestionIndex.value = idx
  questionSheetOpen.value = false
  resetChat()
}
const isFavorite = (id: string | undefined) => (id ? favoriteIds.value.has(id) : false)
const toggleFavorite = (id: string | undefined) => {
  if (!id) return
  const next = new Set(favoriteIds.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  favoriteIds.value = next
  localStorage.setItem(FAVORITE_STORAGE_KEY, JSON.stringify([...next]))
}

const textInput = ref('')
const guidanceInput = ref('')
const uploadedAudioFile = ref<File | null>(null)
const audioSource = ref<'record' | 'upload'>('record')
const fileInputRef = ref<HTMLInputElement | null>(null)
const isDragOver = ref(false)
const isLoading = ref(false)
const evaluationResult = ref<EvalResult | null>(null)
const streamingFeedback = ref('')
const messages = ref<Array<{ content: string; isUser: boolean; timestamp: string }>>([])

const {
  isRecording,
  audioBlob,
  audioUrl,
  startRecording,
  stopRecording,
  getAudioFile,
  reset: resetAudio,
} = useAudioRecorder()

const hasSelectedAudio = computed(() => {
  if (audioSource.value === 'upload') return !!uploadedAudioFile.value
  return !!audioBlob.value
})

watch(
  currentQuestion,
  (q) => {
    guidanceInput.value = q?.guidance || ''
  },
  { immediate: true }
)

watch(currentType, () => {
  currentQuestionIndex.value = 0
  showSegments.value = false
  resetChat()
})

const toggleRecording = async () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    try {
      await startRecording()
    } catch (error) {
      showError('无法访问麦克风，请检查权限设置')
    }
  }
}

const openFilePicker = () => {
  fileInputRef.value?.click()
}

const setUploadedAudioFile = (file: File) => {
  const lowerName = file.name.toLowerCase()
  const valid = lowerName.endsWith('.pcm') || lowerName.endsWith('.mp3')
  if (!valid) {
    showError('仅支持单个 .pcm 或 .mp3 文件。')
    return false
  }

  uploadedAudioFile.value = file
  audioSource.value = 'upload'
  return true
}

const onFileSelected = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  setUploadedAudioFile(file)
  target.value = ''
}

const onDropAudio = (event: DragEvent) => {
  isDragOver.value = false
  const file = event.dataTransfer?.files?.[0]
  if (!file) return
  setUploadedAudioFile(file)
}

const clearUploadedFile = () => {
  uploadedAudioFile.value = null
  if (audioSource.value === 'upload') {
    audioSource.value = audioBlob.value ? 'record' : 'upload'
  }
}

const clearRecordedAudio = () => {
  resetAudio()
  if (audioSource.value === 'record') {
    audioSource.value = uploadedAudioFile.value ? 'upload' : 'record'
  }
}

const formatTime = () => {
  return new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const submitCombined = async () => {
  const file =
    audioSource.value === 'upload'
      ? uploadedAudioFile.value
      : await getAudioFile()
  if (!file || isLoading.value) return

  const questionText = currentQuestion.value?.content || ''
  const userExtra = textInput.value.trim()
  const baseGuidance = (currentQuestion.value?.prompt ?? currentQuestion.value?.guidance) || ''
let guidance = guidanceInput.value.trim() || baseGuidance
  if (userExtra) {
    guidance += `\n用户补充问题：${userExtra}`
  }

  await submitEvaluationData(file, questionText, guidance)
  if (audioSource.value === 'upload') {
    clearUploadedFile()
  } else {
    clearRecordedAudio()
  }
  textInput.value = ''
}

const submitEvaluationData = async (file: File, questionText: string, guidance: string) => {
  isLoading.value = true
  evaluationResult.value = null
  streamingFeedback.value = ''

  try {
    await submitEvaluation(file, questionText, guidance, (chunk) => {
      if (chunk.type === 'evaluation' && chunk.data) {
        evaluationResult.value = chunk.data as EvalResult
      } else if (chunk.type === 'feedback_chunk' && typeof chunk.data === 'string') {
        streamingFeedback.value += chunk.data
      } else if (chunk.type === 'done') {
        incrementPracticeCount(currentQuestion.value?.id)
        if (streamingFeedback.value) {
          messages.value.push({
            content: streamingFeedback.value,
            isUser: false,
            timestamp: formatTime(),
          })
          streamingFeedback.value = ''
        }
        isLoading.value = false
      } else if (chunk.type === 'error') {
        showError(chunk.detail?.trim() || '发生未知错误')
        isLoading.value = false
      } else if (chunk.type === 'info') {
        console.info(chunk.detail)
      }
    })
  } catch (error) {
    showError(error instanceof Error ? error.message : String(error) || '提交失败')
    isLoading.value = false
  }
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < questionsByType.value.length - 1) {
    currentQuestionIndex.value++
    resetChat()
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    resetChat()
  }
}

const resetChat = () => {
  messages.value = []
  evaluationResult.value = null
  streamingFeedback.value = ''
  textInput.value = ''
  clearUploadedFile()
  clearRecordedAudio()
}
</script>
