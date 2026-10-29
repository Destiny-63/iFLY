<template>
  <SidebarProvider>
    <Sidebar />

    <SidebarInset>
      <header class="flex h-14 items-center gap-2 border-b bg-card px-4">
        <SidebarTrigger />
        <div class="text-sm text-muted-foreground">{{ $t('sidebar.coreFeatures') }} / {{ $t('sidebar.personalizedPractice') }}</div>
      </header>

      <div class="flex-1 overflow-auto p-4">
        <div class="mx-auto max-w-3xl space-y-6">
          <div class="flex items-center gap-3">
            <div class="flex size-12 items-center justify-center rounded-lg bg-primary/10">
              <Target class="size-6 text-primary" />
            </div>
            <div>
              <h1 class="text-2xl font-semibold">{{ $t('sidebar.personalizedPractice') }}</h1>
              <p class="text-sm text-muted-foreground">{{ $t('coreFeatures.personalizedPracticeDesc') }}</p>
            </div>
          </div>

          <div class="grid gap-4 sm:grid-cols-3">
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm font-medium text-muted-foreground">{{ $t('profile.completed') }}</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold">{{ stat?.completed ?? 0 }}</div>
                <p class="text-xs text-muted-foreground">{{ $t('profile.total') }} {{ stat?.total ?? 50 }}</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm font-medium text-muted-foreground">{{ $t('profile.lastUsed') }}</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-lg font-semibold">{{ formatDate(stat?.lastUsed) }}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm font-medium text-muted-foreground">{{ $t('coreFeatures.trend') }}</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="flex gap-1">
                  <span
                    v-for="(v, i) in (stat?.trend ?? [])"
                    :key="i"
                    class="h-6 flex-1 rounded-sm bg-primary/30"
                    :style="{ opacity: 0.3 + (v / 8) * 0.7 }"
                  />
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>{{ $t('sidebar.personalizedPractice') }}</CardTitle>
              <CardDescription>根据你的练习记录与评测结果，智能推荐薄弱项进行针对性练习。</CardDescription>
            </CardHeader>
            <CardContent>
              <Button size="lg" disabled>
                {{ $t('coreFeatures.comingSoon') }}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar'
import Sidebar from '@/components/Sidebar.vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Target } from 'lucide-vue-next'

const stats = ref<{ coreFeaturesStats?: { id: string; completed?: number; total?: number; lastUsed?: string; trend?: number[] }[] } | null>(null)
const stat = computed(() => stats.value?.coreFeaturesStats?.find((s) => s.id === 'personalizedPractice'))

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
