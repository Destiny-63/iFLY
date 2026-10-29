<template>
  <SidebarProvider>
    <Sidebar />

    <SidebarInset>
      <header class="flex h-14 items-center gap-2 border-b bg-card px-4">
        <SidebarTrigger />
        <div class="text-sm text-muted-foreground">{{ $t('topicSpeaking.sectionTitle') }} / {{ $t('topicSpeaking.topic') }}</div>
      </header>
      <div class="flex min-h-0 flex-1 flex-col">
        <!-- 题目区域 -->
        <div class="border-b bg-card p-4">
          <template v-if="topics.length">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-4">
                <h2 class="flex items-baseline gap-1.5">
                  <span class="text-sm font-medium text-muted-foreground">{{ $t('topicSpeaking.question') }}</span>
                  <span class="text-3xl font-semibold tabular-nums">{{ currentTopicIndex + 1 }}</span>
                  <span class="text-sm text-muted-foreground">/ {{ topics.length }}</span>
                </h2>
                <Badge variant="outline">{{ $t('sidebar.topicSpeaking') }}</Badge>
              </div>
              <div class="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  :disabled="currentTopicIndex === 0"
                  @click="previousTopic"
                >
                  {{ $t('topicSpeaking.previous') }}
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  :disabled="currentTopicIndex === topics.length - 1"
                  @click="nextTopic"
                >
                  {{ $t('topicSpeaking.next') }}
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  class="h-9 w-9 shrink-0 p-0"
                  :aria-label="$t('topicSpeaking.questionList')"
                  @click="topicSheetOpen = true"
                >
                  <LayoutGrid class="size-4" />
                </Button>
              </div>
            </div>

            <Sheet v-model:open="topicSheetOpen">
              <SheetContent side="right" class="w-full sm:max-w-md">
                <SheetHeader>
                  <SheetTitle>{{ $t('topicSpeaking.questionList') }}</SheetTitle>
                  <SheetDescription>{{ $t('topicSpeaking.questionListDesc') }}</SheetDescription>
                </SheetHeader>
                <div class="mt-4 grid grid-cols-5 gap-3 sm:grid-cols-6">
                  <button
                    v-for="(t, idx) in topics"
                    :key="t.id"
                    type="button"
                    class="flex size-10 min-w-0 items-center justify-center rounded-md text-base font-semibold tabular-nums transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                    :class="idx === currentTopicIndex ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground hover:bg-muted/80'"
                    @click="goToTopic(idx)"
                  >
                    {{ idx + 1 }}
                  </button>
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
                        variant="ghost"
                        size="icon"
                        class="h-8 w-8 shrink-0"
                        :class="isFavorite(currentTopic?.id) ? 'text-primary' : 'text-muted-foreground'"
                        :aria-label="isFavorite(currentTopic?.id) ? $t('home.unfavorite') : $t('home.favorite')"
                        @click="toggleFavorite(currentTopic?.id)"
                      >
                        <Star
                          class="size-4"
                          :class="{ 'fill-current': isFavorite(currentTopic?.id) }"
                        />
                      </Button>
                    </div>
                  </div>
                  <!-- 题目说明与话题 -->
                  <p class="text-sm text-muted-foreground">{{ $t('topicSpeaking.topicPrompt') }}</p>
                  <p class="text-xl font-semibold">《{{ currentTopic?.topic }}》</p>
                </CardContent>
              </Card>
            </div>
          </template>
          <div v-else class="rounded-xl border border-dashed bg-muted/30 p-8 text-center text-muted-foreground">
            {{ $t('topicSpeaking.noTopics') }}
          </div>
        </div>

        <!-- 聊天区域 -->
        <ScrollArea class="flex-1">
          <div class="space-y-4 p-4">
            <TopicSpeakingResult v-if="evaluationResult" :result="evaluationResult" />

            <div v-for="(message, index) in messages" :key="index">
              <GuidanceRichText :content="message.content" :timestamp="message.timestamp" />
            </div>

            <div v-if="isLoading" class="flex flex-col items-center justify-center gap-2 p-4">
              <Spinner />
              <span class="text-sm text-muted-foreground">{{ $t('topicSpeaking.evaluating') }}</span>
              <span class="text-xs text-muted-foreground">{{ $t('topicSpeaking.evaluatingHint') }}</span>
            </div>

            <div v-if="streamingFeedback">
              <GuidanceRichText :content="streamingFeedback" />
            </div>
          </div>
        </ScrollArea>

        <!-- 输入区域 -->
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
                  :disabled="isLoading || isRecording || !hasSelectedAudio || !topics.length"
                  @click="submitTopic"
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
import { ref, computed, onMounted } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import TopicSpeakingResult from '@/components/TopicSpeakingResult.vue'
import GuidanceRichText from '@/components/GuidanceRichText.vue'
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
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
import { BookOpen, Gauge, LayoutGrid, Mic, Plus, SendHorizontal, Star, Tag } from 'lucide-vue-next'
import { useTopicBank } from '@/composables/useTopicBank'
import { resolveI18n, resolveI18nTags } from '@/types/questions'
import { submitTopicSpeaking, type TopicSpeakingResult as TopicResult } from '@/api/topicSpeaking'
import { useAudioRecorder } from '@/composables/useAudioRecorder'
import { useSettings } from '@/composables/useSettings'
import { useI18n } from 'vue-i18n'

useSettings()

const { locale } = useI18n()
const { getTopics, load } = useTopicBank()
onMounted(() => load())

const topics = computed(() => getTopics())
const currentTopicIndex = ref(0)
const currentTopic = computed(() => topics.value[currentTopicIndex.value])

const resolvedTitle = computed(() => resolveI18n(currentTopic.value?.title, locale.value))
const resolvedDifficulty = computed(() => resolveI18n(currentTopic.value?.difficulty, locale.value))
const resolvedTags = computed(() => resolveI18nTags(currentTopic.value?.tags, locale.value))

const FAVORITE_STORAGE_KEY = 'ifly-topic-favorites'
const favoriteIds = ref<Set<string>>(new Set(JSON.parse(localStorage.getItem(FAVORITE_STORAGE_KEY) ?? '[]')))
const isFavorite = (id: string | undefined) => (id ? favoriteIds.value.has(id) : false)
const toggleFavorite = (id: string | undefined) => {
  if (!id) return
  const next = new Set(favoriteIds.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  favoriteIds.value = next
  localStorage.setItem(FAVORITE_STORAGE_KEY, JSON.stringify([...next]))
}

const topicSheetOpen = ref(false)
const errorDialogOpen = ref(false)
const errorMessage = ref('')
const showError = (msg: string) => {
  errorMessage.value = msg
  errorDialogOpen.value = true
}
const goToTopic = (idx: number) => {
  currentTopicIndex.value = idx
  topicSheetOpen.value = false
  resetChat()
}

const uploadedAudioFile = ref<File | null>(null)
const audioSource = ref<'record' | 'upload'>('record')
const fileInputRef = ref<HTMLInputElement | null>(null)
const isDragOver = ref(false)
const isLoading = ref(false)
const evaluationResult = ref<TopicResult | null>(null)
const textInput = ref('')
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

const toggleRecording = async () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    try {
      await startRecording()
    } catch {
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

const submitTopic = async () => {
  const file =
    audioSource.value === 'upload'
      ? uploadedAudioFile.value
      : await getAudioFile()
  if (!file || isLoading.value || !currentTopic.value) return

  isLoading.value = true
  evaluationResult.value = null
  streamingFeedback.value = ''

  try {
    await submitTopicSpeaking(file, currentTopic.value.topic, (chunk) => {
      if (chunk.type === 'evaluation' && chunk.data) {
        evaluationResult.value = chunk.data as TopicResult
      } else if (chunk.type === 'evaluation_update' && chunk.data && typeof chunk.data === 'object' && 'psc_score' in chunk.data) {
        if (evaluationResult.value) {
          evaluationResult.value = { ...evaluationResult.value, psc_score: chunk.data.psc_score }
        }
      } else if (chunk.type === 'feedback_chunk' && typeof chunk.data === 'string') {
        streamingFeedback.value += chunk.data
      } else if (chunk.type === 'done') {
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

  if (audioSource.value === 'upload') {
    clearUploadedFile()
  } else {
    clearRecordedAudio()
  }
}

const previousTopic = () => {
  if (currentTopicIndex.value > 0) {
    currentTopicIndex.value--
    resetChat()
  }
}

const nextTopic = () => {
  if (currentTopicIndex.value < topics.value.length - 1) {
    currentTopicIndex.value++
    resetChat()
  }
}

const resetChat = () => {
  textInput.value = ''
  messages.value = []
  evaluationResult.value = null
  streamingFeedback.value = ''
  clearUploadedFile()
  clearRecordedAudio()
}
</script>
