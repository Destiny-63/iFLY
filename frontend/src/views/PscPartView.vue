<template>
  <SidebarProvider>
    <Sidebar />

    <SidebarInset>
      <header class="flex h-14 items-center gap-2 border-b bg-card px-4">
        <SidebarTrigger />
        <div class="text-sm text-muted-foreground">{{ $t('sidebar.pscExamParts') }} / {{ partName }}</div>
      </header>

      <div class="flex-1 overflow-auto p-4">
        <div class="mx-auto max-w-3xl space-y-6">
          <div class="flex items-center gap-3">
            <div class="flex size-12 items-center justify-center rounded-lg bg-primary/10">
              <component :is="partIcon" class="size-6 text-primary" />
            </div>
            <div>
              <h1 class="text-2xl font-semibold">{{ partName }}</h1>
              <p class="text-sm text-muted-foreground">{{ partDesc }}</p>
            </div>
          </div>

          <!-- 统计卡片与功能入口暂不展示
          <div v-if="stat" class="grid gap-4 sm:grid-cols-3">
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm font-medium text-muted-foreground">{{ $t('profile.examCount') }}</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold">{{ stat.examCount ?? 0 }}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm font-medium text-muted-foreground">{{ $t('profile.avgScore') }}</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold">{{ stat.avgScore ?? 0 }}</div>
                <p class="text-xs text-muted-foreground">/ 100</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm font-medium text-muted-foreground">{{ $t('profile.lastUsed') }}</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-lg font-semibold">{{ formatDate(stat.lastDate) }}</div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>{{ partName }}</CardTitle>
              <CardDescription>{{ partDesc }}</CardDescription>
            </CardHeader>
            <CardContent>
              <Button size="lg" disabled>
                {{ $t('coreFeatures.comingSoon') }}
              </Button>
            </CardContent>
          </Card>
          -->
        </div>
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar'
import Sidebar from '@/components/Sidebar.vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Type, MessageSquareText, ListChecks, FileText } from 'lucide-vue-next'
import { pscParts } from '@/data/mock'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const { t } = useI18n()

const PART_ICONS = {
  singleCharacterReading: Type,
  wordReading: MessageSquareText,
  choiceJudgment: ListChecks,
  passageReading: FileText,
} as const

const partId = computed(() => route.params.partId as string)
const partMeta = computed(() => pscParts.find((p) => p.id === partId.value))
const partName = computed(() => (partMeta.value ? t(`sidebar.${partMeta.value.id}`) : partId.value))
const partDesc = computed(() => partMeta.value?.description ?? '')
const partIcon = computed(() => PART_ICONS[partId.value as keyof typeof PART_ICONS] ?? FileText)

const stats = ref<{ pscPartsStats?: { id: string; examCount?: number; avgScore?: number; lastDate?: string }[] } | null>(null)
const stat = computed(() => stats.value?.pscPartsStats?.find((s) => s.id === partId.value))

function formatDate(d?: string) {
  if (!d) return '-'
  try {
    return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
  } catch {
    return d
  }
}

onMounted(async () => {
  try {
    const res = await fetch('/data/stats.json')
    if (res.ok) stats.value = await res.json()
  } catch (_) {}
})
</script>
