<template>
  <SidebarProvider>
    <Sidebar />

    <SidebarInset>
      <header class="flex h-14 items-center gap-2 border-b bg-card px-4">
        <SidebarTrigger />
        <div class="text-sm text-muted-foreground">{{ $t('sidebar.mockExam') }} / {{ $t('sidebar.examStats') }}</div>
      </header>

      <div class="flex-1 overflow-auto p-4">
        <div class="mx-auto max-w-3xl space-y-6">
          <div class="flex items-center gap-3">
            <div class="flex size-12 items-center justify-center rounded-lg bg-primary/10">
              <BarChart3 class="size-6 text-primary" />
            </div>
            <div>
              <h1 class="text-2xl font-semibold">{{ $t('sidebar.examStats') }}</h1>
              <p class="text-sm text-muted-foreground">{{ $t('sidebar.examStatsDesc') }}</p>
            </div>
          </div>

          <!--Card>
            <CardHeader>
              <CardTitle>{{ $t('profile.recentExams') }}</CardTitle>
              <CardDescription>{{ $t('profile.recentExamsDesc') }}</CardDescription>
            </CardHeader>
            <CardContent>
              <div v-if="recentExams.length" class="space-y-2">
                <div
                  v-for="(exam, i) in recentExams"
                  :key="i"
                  class="flex items-center justify-between rounded-md border px-3 py-2"
                >
                  <span class="text-sm">{{ formatDate(exam.date) }}</span>
                  <span class="text-sm text-muted-foreground">{{ typeLabel(exam.type) }}</span>
                  <span class="font-semibold">{{ exam.score }} 分</span>
                </div>
              </div>
              <p v-else class="text-sm text-muted-foreground">{{ $t('profile.noData') }}</p>
            </CardContent>
          </Card-->
        </div>
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const typeLabel = (type: string) => t(`sidebar.${type}`) || type
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar'
import Sidebar from '@/components/Sidebar.vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart3 } from 'lucide-vue-next'

const recentExams = ref<{ date: string; type: string; score: number; totalQuestions?: number }[]>([])

function formatDate(d: string) {
  try {
    return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
  } catch {
    return d
  }
}

onMounted(async () => {
  try {
    const res = await fetch('/data/stats.json')
    if (res.ok) {
      const data = await res.json()
      recentExams.value = data.recentExams ?? []
    }
  } catch (_) {}
})
</script>
