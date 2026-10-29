<template>
  <SidebarProvider>
    <Sidebar />

    <SidebarInset>
      <header class="flex h-14 items-center gap-2 border-b bg-card px-4">
        <SidebarTrigger />
        <div class="text-sm text-muted-foreground">{{ $t('sidebar.coreFeatures') }} / {{ $t('sidebar.questionBank') }}</div>
      </header>

      <div class="flex-1 overflow-auto p-4">
        <div class="mx-auto max-w-3xl space-y-6">
          <div class="flex items-center gap-3">
            <div class="flex size-12 items-center justify-center rounded-lg bg-primary/10">
              <Database class="size-6 text-primary" />
            </div>
            <div>
              <h1 class="text-2xl font-semibold">{{ $t('sidebar.questionBank') }}</h1>
              <p class="text-sm text-muted-foreground">{{ $t('coreFeatures.questionBankDesc') }}</p>
            </div>
          </div>

          <div class="grid gap-4 sm:grid-cols-3">
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm font-medium text-muted-foreground">{{ $t('profile.browsed') }}</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold">{{ stat?.browsed ?? 0 }}</div>
                <p class="text-xs text-muted-foreground">{{ $t('profile.count') }}</p>
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
                    :style="{ opacity: 0.3 + (v / 15) * 0.7 }"
                  />
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>{{ $t('sidebar.questionBank') }}</CardTitle>
              <CardDescription>按题型（字、词语、句子、文章）浏览题目，支持按难度、标签筛选，收藏常练题目。</CardDescription>
            </CardHeader>
            <CardContent>
              <div class="flex gap-2">
                <Button variant="outline" @click="router.push('/question-type/character')">
                  {{ $t('sidebar.character') }}
                </Button>
                <Button variant="outline" @click="router.push('/question-type/word')">
                  {{ $t('sidebar.word') }}
                </Button>
                <Button variant="outline" @click="router.push('/question-type/sentence')">
                  {{ $t('sidebar.sentence') }}
                </Button>
                <Button variant="outline" @click="router.push('/question-type/article')">
                  {{ $t('sidebar.article') }}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar'
import Sidebar from '@/components/Sidebar.vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Database } from 'lucide-vue-next'

const router = useRouter()
const stats = ref<{ coreFeaturesStats?: { id: string; browsed?: number; lastUsed?: string; trend?: number[] }[] } | null>(null)
const stat = computed(() => stats.value?.coreFeaturesStats?.find((s) => s.id === 'questionBank'))

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
