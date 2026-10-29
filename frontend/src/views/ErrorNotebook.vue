<template>
  <SidebarProvider>
    <Sidebar />

    <SidebarInset>
      <header class="flex h-14 items-center gap-2 border-b bg-card px-4">
        <SidebarTrigger />
        <div class="text-sm text-muted-foreground">{{ $t('sidebar.coreFeatures') }} / {{ $t('sidebar.errorNotebook') }}</div>
      </header>

      <div class="flex-1 overflow-auto p-4">
        <div class="mx-auto max-w-3xl space-y-6">
          <div class="flex items-center gap-3">
            <div class="flex size-12 items-center justify-center rounded-lg bg-primary/10">
              <BookMarked class="size-6 text-primary" />
            </div>
            <div>
              <h1 class="text-2xl font-semibold">{{ $t('sidebar.errorNotebook') }}</h1>
              <p class="text-sm text-muted-foreground">{{ $t('coreFeatures.errorNotebookDesc') }}</p>
            </div>
          </div>

          <!-- 统计卡片与功能入口暂不展示
          <div class="grid gap-4 sm:grid-cols-3">
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm font-medium text-muted-foreground">{{ $t('profile.count') }}</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold">{{ stat?.count ?? 0 }}</div>
                <p class="text-xs text-muted-foreground">{{ $t('coreFeatures.errorCountUnit') }}</p>
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
                    :style="{ opacity: 0.3 + (v / 4) * 0.7 }"
                  />
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>{{ $t('sidebar.errorNotebook') }}</CardTitle>
              <CardDescription>收录评测中的发音错误、缺陷与扣分项，支持按类型筛选与定期复习。</CardDescription>
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
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar'
import Sidebar from '@/components/Sidebar.vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { BookMarked } from 'lucide-vue-next'

const stats = ref<{ coreFeaturesStats?: { id: string; count?: number; lastUsed?: string; trend?: number[] }[] } | null>(null)
const stat = computed(() => stats.value?.coreFeaturesStats?.find((s) => s.id === 'errorNotebook'))

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
