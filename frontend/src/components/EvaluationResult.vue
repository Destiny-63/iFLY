<template>
  <Card v-if="result" class="mb-4">
    <CardHeader>
      <CardTitle class="text-lg">{{ $t('evaluation.title') }}</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="grid grid-cols-2 gap-4 md:grid-cols-4">
        <div class="flex flex-col">
          <span class="text-sm text-muted-foreground">{{ $t('evaluation.totalScore') }}</span>
          <span class="text-2xl font-bold">{{ result.total_score.toFixed(2) }}</span>
        </div>
        <div class="flex flex-col">
          <span class="text-sm text-muted-foreground">{{ $t('evaluation.accuracy') }}</span>
          <span class="text-2xl font-bold">{{ result.accuracy_score?.toFixed(2) || 'N/A' }}</span>
        </div>
        <div class="flex flex-col">
          <span class="text-sm text-muted-foreground">{{ $t('evaluation.fluency') }}</span>
          <span class="text-2xl font-bold">{{ result.fluency_score?.toFixed(2) || 'N/A' }}</span>
        </div>
        <div class="flex flex-col">
          <span class="text-sm text-muted-foreground">{{ $t('evaluation.integrity') }}</span>
          <span class="text-2xl font-bold">{{ result.integrity_score?.toFixed(2) || 'N/A' }}</span>
        </div>
      </div>

      <div class="mt-4 rounded-md border bg-muted/40 p-3">
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium">{{ $t('evaluation.learningStar') }}</span>
          <div class="flex items-center gap-1">
            <span
              v-for="i in 5"
              :key="i"
              class="text-lg"
              :class="i <= starLevel ? 'text-primary' : 'text-muted-foreground/40'"
            >
              ★
            </span>
            <span class="ml-2 text-xs text-muted-foreground">{{ starLevel }}/5</span>
          </div>
        </div>
      </div>

      <Tabs v-model="activeTab" class="mt-4">
        <TabsList>
          <TabsTrigger value="summary">{{ $t('evaluation.summary') }}</TabsTrigger>
          <TabsTrigger value="xml">{{ $t('evaluation.xmlData') }}</TabsTrigger>
        </TabsList>
        <TabsContent value="summary" class="mt-4">
          <div class="space-y-2 text-sm">
            <div>
              <span class="font-medium">{{ $t('evaluation.toneScore') }}</span>
              {{ result.tone_score?.toFixed(2) || 'N/A' }}
            </div>
            <div>
              <span class="font-medium">{{ $t('evaluation.phoneScore') }}</span>
              {{ result.phone_score?.toFixed(2) || 'N/A' }}
            </div>
          </div>
        </TabsContent>
        <TabsContent value="xml" class="mt-4">
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-sm text-muted-foreground">{{ $t('evaluation.fullXmlData') }}</span>
              <Button
                v-if="result.raw_xml"
                variant="outline"
                size="sm"
                @click="copyXml"
              >
                {{ $t('evaluation.copy') }}
              </Button>
            </div>
            <ScrollArea class="h-64 rounded-md border bg-muted/50 p-4">
              <pre class="text-xs font-mono whitespace-pre-wrap break-words">{{ result.raw_xml || $t('evaluation.noXmlData') }}</pre>
            </ScrollArea>
          </div>
        </TabsContent>
      </Tabs>
    </CardContent>
  </Card>

  <!-- 复制反馈弹窗 -->
  <Dialog v-model:open="copyDialogOpen">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>{{ copyDialogMessage }}</DialogTitle>
      </DialogHeader>
      <DialogFooter>
        <Button @click="copyDialogOpen = false">{{ $t('evaluation.confirm') }}</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from './ui/dialog'
import { Tabs, TabsList, TabsTrigger, TabsContent } from './ui/tabs'
import { ScrollArea } from './ui/scroll-area'
import { Button } from './ui/button'
import type { EvaluationResult } from '@/api/evaluation'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Props {
  result: EvaluationResult | null
}

const props = defineProps<Props>()

const activeTab = ref('summary')
const copyDialogOpen = ref(false)
const copyDialogMessage = ref('')

const starLevel = computed(() => {
  const score = props.result?.total_score ?? 0
  if (score >= 90) return 5
  if (score >= 80) return 4
  if (score >= 70) return 3
  if (score >= 60) return 2
  return 1
})

const copyXml = async () => {
  if (!props.result?.raw_xml) return
  try {
    await navigator.clipboard.writeText(props.result.raw_xml)
    copyDialogMessage.value = t('evaluation.copied')
    copyDialogOpen.value = true
  } catch (error) {
    console.error('复制失败:', error)
    copyDialogMessage.value = t('evaluation.copyFailed')
    copyDialogOpen.value = true
  }
}
</script>
