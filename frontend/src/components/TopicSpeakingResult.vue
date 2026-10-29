<template>
  <Card v-if="result" class="mb-4">
    <CardHeader>
      <CardTitle class="text-lg">{{ $t('topicSpeaking.resultTitle') }}</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-4">
        <div class="flex flex-wrap gap-4 text-sm">
          <div>
            <span class="text-muted-foreground">{{ $t('topicSpeaking.duration') }}：</span>
            <span class="font-medium">{{ result.duration_seconds }} {{ $t('topicSpeaking.seconds') }}</span>
          </div>
          <div v-if="result.time_penalty.deduct > 0">
            <span class="text-muted-foreground">{{ $t('topicSpeaking.timePenalty') }}：</span>
            <span class="font-medium text-destructive">-{{ result.time_penalty.deduct }} {{ $t('topicSpeaking.points') }}</span>
            <span class="text-muted-foreground ml-1">({{ result.time_penalty.reason }})</span>
          </div>
        </div>

        <div v-if="result.transcript" class="rounded-md border bg-muted/40 p-3">
          <span class="text-sm font-medium text-muted-foreground">{{ $t('topicSpeaking.transcript') }}</span>
          <p class="mt-2 text-sm">{{ result.transcript }}</p>
        </div>

        <!-- PSC 命题说话总分（40 分制） -->
        <div v-if="result.psc_score?.total != null" class="rounded-md border bg-primary/5 p-4">
          <span class="text-sm font-medium text-muted-foreground">{{ $t('topicSpeaking.pscTotalScore') }}</span>
          <p class="mt-1 text-3xl font-bold tabular-nums">{{ result.psc_score.total }} <span class="text-lg font-normal text-muted-foreground">/ 40</span></p>
          <div v-if="hasPscDeductions" class="mt-2 flex flex-wrap gap-3 text-sm text-muted-foreground">
            <span v-if="result.psc_score.dim1_deduct != null">{{ $t('topicSpeaking.dim1Phonetic') }} -{{ result.psc_score.dim1_deduct }}</span>
            <span v-if="result.psc_score.dim2_deduct != null">{{ $t('topicSpeaking.dim2Grammar') }} -{{ result.psc_score.dim2_deduct }}</span>
            <span v-if="result.psc_score.dim3_deduct != null">{{ $t('topicSpeaking.dim3Fluency') }} -{{ result.psc_score.dim3_deduct }}</span>
          </div>
        </div>

        <!-- ISE 发音参考（0–100 分，仅作参考） -->
        <div v-if="result.ise_result" class="rounded-md border border-dashed bg-muted/30 p-3">
          <span class="text-sm font-medium text-muted-foreground">{{ $t('topicSpeaking.iseReference') }}</span>
          <div class="mt-2 grid grid-cols-2 gap-4 md:grid-cols-4">
            <div class="flex flex-col">
              <span class="text-xs text-muted-foreground">{{ $t('topicSpeaking.iseTotal') }}</span>
              <span class="text-xl font-semibold tabular-nums">{{ (result.ise_result.total_score ?? 0).toFixed(1) }}</span>
            </div>
            <div class="flex flex-col">
              <span class="text-xs text-muted-foreground">{{ $t('evaluation.accuracy') }}</span>
              <span class="text-xl font-semibold tabular-nums">{{ (result.ise_result.accuracy_score ?? result.ise_result.phone_score ?? 0).toFixed(1) }}</span>
            </div>
            <div class="flex flex-col">
              <span class="text-xs text-muted-foreground">{{ $t('evaluation.fluency') }}</span>
              <span class="text-xl font-semibold tabular-nums">{{ (result.ise_result.fluency_score ?? 0).toFixed(1) }}</span>
            </div>
            <div class="flex flex-col">
              <span class="text-xs text-muted-foreground">{{ $t('evaluation.integrity') }}</span>
              <span class="text-xl font-semibold tabular-nums">{{ (result.ise_result.integrity_score ?? 0).toFixed(1) }}</span>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import type { TopicSpeakingResult } from '@/api/topicSpeaking'

const props = defineProps<{
  result: TopicSpeakingResult | null
}>()

const hasPscDeductions = computed(() => {
  const p = props.result?.psc_score
  return (
    (p?.dim1_deduct != null && p.dim1_deduct > 0) ||
    (p?.dim2_deduct != null && p.dim2_deduct > 0) ||
    (p?.dim3_deduct != null && p.dim3_deduct > 0)
  )
})
</script>
