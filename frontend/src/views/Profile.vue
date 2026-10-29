<template>
  <SidebarProvider>
    <Sidebar />

    <SidebarInset>
      <header class="flex h-14 items-center gap-2 border-b bg-card px-4">
        <SidebarTrigger />
        <div class="text-sm font-medium">{{ $t('profile.title') }}</div>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="mx-auto max-w-6xl space-y-6">
          <!-- 主标题 -->
          <div>
            <h1 class="text-2xl font-bold tracking-tight">{{ $t('profile.title') }}</h1>
            <p class="mt-1 text-sm text-muted-foreground">{{ $t('profile.subtitle') }}</p>
          </div>

          <!-- 第一行：个人信息 Card + Score Trend Card -->
          <div class="grid gap-6 lg:grid-cols-[minmax(0,4fr)_minmax(0,8fr)]">
            <Card class="overflow-hidden border bg-card">
              <CardHeader class="pb-2">
                <CardTitle class="text-base">{{ $t('profile.userInfo') }}</CardTitle>
                <CardDescription>{{ $t('profile.userInfoDesc') }}</CardDescription>
              </CardHeader>
              <CardContent class="space-y-4">
                <div class="grid gap-4 text-sm sm:grid-cols-2">
                  <Field>
                    <FieldLabel>{{ $t('profile.displayName') }}</FieldLabel>
                    <FieldContent>
                      <div v-if="!editingName" class="flex items-center gap-1.5">
                        <span class="truncate font-medium">{{ profile?.user?.name ?? '—' }}</span>
                        <button type="button" class="shrink-0 rounded p-0.5 text-muted-foreground hover:bg-muted hover:text-foreground" :aria-label="$t('profile.edit')" @click="startEditName">
                          <Pencil class="size-3.5" />
                        </button>
                      </div>
                      <Input v-else ref="nameInputRef" v-model="editNameValue" class="h-8 font-medium" @blur="saveName" @keydown.enter="saveName" @keydown.escape="cancelEditName" />
                    </FieldContent>
                  </Field>
                  <Field>
                    <FieldLabel>{{ $t('profile.targetLevel') }}</FieldLabel>
                    <FieldContent>
                      <Select v-model="targetLevelKey">
                        <SelectTrigger class="h-8 font-medium">
                          <SelectValue :placeholder="$t('profile.targetLevel')" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem v-for="opt in targetLevelOptions" :key="opt.value" :value="opt.value">
                            {{ $t(opt.labelKey) }}
                          </SelectItem>
                        </SelectContent>
                      </Select>
                    </FieldContent>
                  </Field>
                  <Field>
                    <FieldLabel>{{ $t('profile.joinDate') }}</FieldLabel>
                    <FieldContent>
                      <span class="tabular-nums text-muted-foreground">{{ profile?.user?.joinDate ?? '—' }}</span>
                    </FieldContent>
                  </Field>
                  <Field>
                    <FieldLabel>{{ $t('profile.email') }}</FieldLabel>
                    <FieldContent>
                      <div v-if="!editingEmail" class="flex items-center gap-1.5">
                        <span class="truncate font-medium">{{ profile?.user?.email ?? '—' }}</span>
                        <button type="button" class="shrink-0 rounded p-0.5 text-muted-foreground hover:bg-muted hover:text-foreground" :aria-label="$t('profile.edit')" @click="startEditEmail">
                          <Pencil class="size-3.5" />
                        </button>
                      </div>
                      <Input v-else ref="emailInputRef" v-model="editEmailValue" class="h-8 font-medium" type="email" @blur="saveEmail" @keydown.enter="saveEmail" @keydown.escape="cancelEditEmail" />
                    </FieldContent>
                  </Field>
                </div>
                <Separator />
                <div class="grid gap-4 text-sm sm:grid-cols-2">
                  <Field>
                    <FieldLabel>{{ $t('profile.memberStatus') }}</FieldLabel>
                    <FieldContent>
                      <span :class="hasMember ? 'font-medium text-primary' : 'text-muted-foreground'">
                        {{ hasMember ? $t('profile.memberActive') : $t('profile.memberInactive') }}
                      </span>
                    </FieldContent>
                  </Field>
                  <Field>
                    <FieldLabel>{{ $t('profile.memberExpire') }}</FieldLabel>
                    <FieldContent>
                      <span class="text-muted-foreground">{{ profile?.model?.memberExpire ?? '—' }}</span>
                    </FieldContent>
                  </Field>
                </div>
              </CardContent>
            </Card>
            <!-- Score Trend：PSC 模拟考试最近测试得分 -->
            <Card>
              <CardHeader class="flex flex-col items-start gap-2 space-y-0 py-4 sm:flex-row">
                <div class="grid flex-1 gap-1">
                  <CardTitle class="text-base">{{ $t('profile.scoreTrend') }}</CardTitle>
                  <CardDescription>{{ $t('profile.scoreTrendDesc') }}</CardDescription>
                </div>
              </CardHeader>
              <CardContent class="px-4 pt-0 sm:px-6">
                <div v-if="scoreTrendData.length" class="h-[220px] w-full">
                  <VisXYContainer
                    :data="scoreTrendData"
                    :height="220"
                    :svg-defs="scoreTrendSvgDefs"
                    :margin="{ left: 40, right: 16, top: 8, bottom: 24 }"
                    :y-domain="[0, 100]"
                  >
                    <VisArea
                      :x="scoreTrendX"
                      :y="scoreTrendY"
                      :color="'url(#fillScoreSelected)'"
                      :opacity="0.4"
                    />
                    <VisLine
                      :x="scoreTrendX"
                      :y="scoreTrendY"
                      :color="scoreTrendSelectedColor"
                      :line-width="1.5"
                    />
                    <VisAxis
                      type="x"
                      :x="scoreTrendX"
                      :tick-line="false"
                      :domain-line="false"
                      :grid-line="false"
                      :num-ticks="6"
                      :tick-format="(d: number) => {
                        const date = new Date(d)
                        return date.toLocaleDateString(locale.value === 'zh' ? 'zh-CN' : 'en-US', { month: 'short', day: 'numeric' })
                      }"
                    />
                    <VisAxis
                      type="y"
                      :num-ticks="5"
                      :tick-line="false"
                      :domain-line="false"
                      :tick-format="(v: number) => String(Math.round(v))"
                    />
                    <VisTooltip :horizontal-shift="12" :vertical-shift="12" />
                    <VisCrosshair
                      :template="scoreTrendTooltipTemplate"
                      :color="scoreTrendSelectedColor"
                    />
                  </VisXYContainer>
                </div>
                <p v-else class="flex h-[200px] items-center justify-center text-sm text-muted-foreground">{{ $t('profile.noData') }}</p>
              </CardContent>
            </Card>
          </div>

          <!-- 第二行：Token 余额与会员 + Token 消耗趋势（两卡并排） -->
          <div class="grid gap-6 lg:grid-cols-[minmax(0,1fr)_1.6fr]">
            <!-- 左侧 Card：Token 余额与会员 -->
            <Card class="overflow-hidden">
              <CardHeader class="pb-2">
                <CardTitle class="text-base font-semibold">{{ $t('profile.tokenBalance') }}</CardTitle>
                <CardDescription class="text-sm text-muted-foreground">{{ $t('profile.tokenMemberDesc') }}</CardDescription>
              </CardHeader>
              <CardContent class="space-y-5">
                <!-- 剩余 Token 突出展示 -->
                <div class="rounded-lg bg-muted/50 px-4 py-3">
                  <p class="text-xs text-muted-foreground">{{ $t('profile.tokensRemaining') }}</p>
                  <p class="text-2xl font-bold tabular-nums">{{ profile?.model?.tokensRemaining?.toLocaleString() ?? 0 }}</p>
                </div>
                <!-- 用量与进度 -->
                <div class="space-y-2">
                  <div class="flex justify-between text-sm">
                    <span class="text-muted-foreground">{{ $t('profile.tokensUsed') }}</span>
                    <span class="tabular-nums">{{ profile?.model?.tokensUsed?.toLocaleString() ?? 0 }} / {{ profile?.model?.tokensTotal?.toLocaleString() ?? 0 }}</span>
                  </div>
                  <div class="h-1.5 rounded-full bg-muted overflow-hidden">
                    <div
                      class="h-full rounded-full bg-primary transition-all"
                      :style="{ width: tokenUsagePercent + '%' }"
                    />
                  </div>
                  <p class="text-xs text-muted-foreground">{{ $t('profile.usedThisWeek') }}: {{ tokenUsedThisWeek.toLocaleString() }}</p>
                </div>
                <Separator />
                <!-- 会员信息 -->
                <div class="grid grid-cols-2 gap-3 text-sm">
                  <div>
                    <p class="text-xs text-muted-foreground">{{ $t('profile.memberLevel') }}</p>
                    <p class="font-medium">{{ resolvedMemberLevel }}</p>
                  </div>
                  <div>
                    <p class="text-xs text-muted-foreground">{{ $t('profile.memberExpire') }}</p>
                    <p class="tabular-nums text-muted-foreground">{{ profile?.model?.memberExpire ?? '—' }}</p>
                  </div>
                </div>
                <Button class="w-full">{{ $t('profile.recharge') }}</Button>
              </CardContent>
            </Card>

            <!-- 右侧 Card：Token 消耗趋势 -->
            <Card class="overflow-hidden">
              <CardHeader class="pb-2">
                <CardTitle class="text-base font-semibold">{{ $t('profile.tokenUsage') }}</CardTitle>
                <CardDescription class="text-sm text-muted-foreground">
                  {{ $t('profile.inputToken') }} / {{ $t('profile.outputToken') }}
                  <template v-if="tokenBarData.length">
                    · {{ $t('profile.inputToken') }}: {{ tokenUsageTotalInput.toLocaleString() }} / {{ $t('profile.outputToken') }}: {{ tokenUsageTotalOutput.toLocaleString() }}
                  </template>
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div class="h-[250px] w-full overflow-x-auto overflow-y-hidden">
                  <template v-if="tokenBarData.length">
                    <div class="min-w-[800px]">
                      <VisXYContainer
                        :data="tokenBarData"
                        :height="250"
                        :margin="{ left: 48, right: 16, top: 8, bottom: 24 }"
                        :auto-margin="false"
                        :y-domain="[0, undefined]"
                      >
                        <VisGroupedBar
                          :x="tokenBarX"
                          :y="tokenBarY"
                          :color="tokenBarColor"
                          :bar-padding="0.1"
                          :rounded-corners="false"
                        />
                        <VisAxis
                          type="x"
                          :x="tokenBarX"
                          :tick-line="false"
                          :domain-line="false"
                          :grid-line="false"
                          :tick-format="(d: number) => {
                            const date = new Date(d)
                            return date.toLocaleDateString(locale.value === 'zh' ? 'zh-CN' : 'en-US', { month: 'short', day: 'numeric' })
                          }"
                        />
                        <VisAxis type="y" :num-ticks="4" :tick-line="false" :domain-line="false" :tick-format="(v: number) => v >= 1000 ? (v / 1000) + 'k' : String(v)" />
                        <VisTooltip :horizontal-shift="12" :vertical-shift="12" />
                        <VisCrosshair
                          :template="tokenBarTooltipTemplate"
                          :color="tokenBarCrosshairColor"
                        />
                      </VisXYContainer>
                    </div>
                  </template>
                  <p v-else class="flex h-full min-h-[200px] items-center justify-center text-sm text-muted-foreground">{{ $t('profile.noData') }}</p>
                </div>
              </CardContent>
              <CardFooter v-if="tokenBarData.length" class="flex flex-wrap items-center justify-between gap-3 border-t py-3">
                <div class="flex items-center gap-4 text-xs text-muted-foreground">
                  <span class="flex items-center gap-1.5">
                    <span class="size-2.5 rounded-sm bg-primary" />
                    {{ $t('profile.inputToken') }}
                  </span>
                  <span class="flex items-center gap-1.5">
                    <span class="size-2.5 rounded-sm bg-primary/70" />
                    {{ $t('profile.outputToken') }}
                  </span>
                </div>
                <p class="text-xs text-muted-foreground">
                  {{ $t('profile.tokenUsageAvg7d') }}: {{ tokenUsageAvg7d }}
                </p>
              </CardFooter>
            </Card>
          </div>

          <!-- 标签页 — 核心功能 / PSC 考试部分 / 题型专项训练 -->
          <Card>
            <CardHeader class="pb-2">
              <CardTitle class="text-base">{{ $t('profile.statsOverview') }}</CardTitle>
              <CardDescription>{{ $t('profile.recentExamsDesc') }}</CardDescription>
            </CardHeader>
            <CardContent>
              <Tabs default-value="core" class="w-full">
                <TabsList class="mb-4 w-full justify-start border-b bg-transparent p-0 h-auto gap-0 rounded-none">
                  <TabsTrigger value="core" class="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:shadow-none">{{ $t('profile.coreFeaturesTab') }}</TabsTrigger>
                  <TabsTrigger value="types" class="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:shadow-none">{{ $t('profile.questionTypesTab') }}</TabsTrigger>
                  <TabsTrigger value="psc" class="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:shadow-none">{{ $t('profile.pscPartsTab') }}</TabsTrigger>
                </TabsList>
                <TabsContent value="core" class="mt-0">
                  <div class="overflow-x-auto">
                    <table class="w-full text-sm">
                      <thead>
                        <tr class="border-b text-left text-muted-foreground">
                          <th class="pb-2 font-medium">{{ $t('profile.featureName') }}</th>
                          <th class="pb-2 font-medium">{{ $t('profile.completed') }}</th>
                          <th class="pb-2 font-medium">{{ $t('profile.lastUsed') }}</th>
                          <th class="pb-2 font-medium w-32">{{ $t('profile.trend') }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="item in coreFeaturesWithLabel"
                          :key="item.id"
                          class="border-b last:border-0"
                        >
                          <td class="py-3 font-medium">{{ item.name }}</td>
                          <td class="py-3 tabular-nums">
                            <template v-if="item.completed != null">{{ item.completed }}</template>
                            <template v-else>{{ item.count ?? item.browsed ?? '—' }}</template>
                          </td>
                          <td class="py-3 text-muted-foreground">{{ item.lastUsed ?? '—' }}</td>
                          <td class="py-3 w-32">
                            <div class="flex h-6 items-end gap-0.5">
                              <div
                                v-for="(v, i) in (item.trend ?? [])"
                                :key="i"
                                class="min-w-[4px] flex-1 rounded-t bg-primary/70"
                                :style="{ height: sparkHeight(v, item.trend) + '%' }"
                              />
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </TabsContent>
                <TabsContent value="psc" class="mt-0">
                  <div class="overflow-x-auto">
                    <table class="w-full text-sm">
                      <thead>
                        <tr class="border-b text-left text-muted-foreground">
                          <th class="pb-2 font-medium">{{ $t('profile.featureName') }}</th>
                          <th class="pb-2 font-medium">{{ $t('profile.examCount') }}</th>
                          <th class="pb-2 font-medium">{{ $t('profile.avgScore') }}</th>
                          <th class="pb-2 font-medium">{{ $t('profile.lastUsed') }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="item in pscPartsWithLabel"
                          :key="item.id"
                          class="border-b last:border-0"
                        >
                          <td class="py-3 font-medium">{{ item.name }}</td>
                          <td class="py-3 tabular-nums">{{ item.examCount ?? 0 }}</td>
                          <td class="py-3 tabular-nums">{{ item.avgScore != null ? item.avgScore + '%' : '—' }}</td>
                          <td class="py-3 text-muted-foreground">{{ item.lastDate ?? '—' }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </TabsContent>
                <TabsContent value="types" class="mt-0">
                  <div class="overflow-x-auto">
                    <table class="w-full text-sm">
                      <thead>
                        <tr class="border-b text-left text-muted-foreground">
                          <th class="pb-2 font-medium">{{ $t('profile.featureName') }}</th>
                          <th class="pb-2 font-medium">{{ $t('profile.count') }}</th>
                          <th class="pb-2 font-medium">{{ $t('profile.accuracy') }}</th>
                          <th class="pb-2 font-medium w-32">{{ $t('profile.trend') }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="item in practiceByTypeWithLabel"
                          :key="item.type"
                          class="border-b last:border-0"
                        >
                          <td class="py-3 font-medium">{{ item.label }}</td>
                          <td class="py-3 tabular-nums">{{ item.count }}</td>
                          <td class="py-3 tabular-nums">{{ item.accuracy != null ? item.accuracy + '%' : '—' }}</td>
                          <td class="py-3 w-32">
                            <div class="flex h-6 items-end gap-0.5">
                              <div
                                v-for="(v, i) in (item.trend ?? [])"
                                :key="i"
                                class="min-w-[4px] flex-1 rounded-t bg-primary/70"
                                :style="{ height: sparkHeight(v, item.trend) + '%' }"
                              />
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          <!-- 每日练习：练习记录热力图（GitHub 风格） -->
          <Card>
            <CardHeader class="flex flex-row items-center justify-between gap-4 pb-2">
              <CardTitle class="text-lg font-semibold">{{ $t('profile.practiceLogTitle') }}</CardTitle>
              <div class="flex items-center gap-2">
                <span class="text-sm text-muted-foreground">
                  {{ totalContributions }} {{ $t('profile.practiceCountUnit') }}
                </span>
                <Select v-model="selectedContributionYear">
                    <SelectTrigger class="h-8 w-[100px]">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem v-for="y in contributionYearOptions" :key="y" :value="String(y)">
                        {{ y }}
                      </SelectItem>
                    </SelectContent>
                </Select>
              </div>
            </CardHeader>
            <CardContent class="p-4 pt-0">
              <div class="overflow-x-auto contribution-heatmap-wrapper">
                <CalendarHeatmap
                  :values="contributionHeatmapValues"
                  :end-date="contributionEndDate"
                  :round="2"
                  :dark-mode="isDark"
                  :range-color="contributionRangeColor"
                  :tooltip-unit="locale.value === 'zh' ? '次' : 'contributions'"
                  :tooltip-formatter="contributionTooltipFormatter"
                />
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useDark } from '@vueuse/core'
import { useI18n } from 'vue-i18n'
import { VisXYContainer, VisAxis, VisArea, VisLine, VisGroupedBar, VisTooltip, VisCrosshair } from '@unovis/vue'
import Sidebar from '@/components/Sidebar.vue'
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Field, FieldLabel, FieldContent } from '@/components/ui/field'
import { Separator } from '@/components/ui/separator'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Pencil } from 'lucide-vue-next'
import { CalendarHeatmap } from 'vue3-calendar-heatmap'
import 'vue3-calendar-heatmap/dist/style.css'
import { resolveI18n } from '@/types/questions'

const targetLevelOptions = [
  { value: '1a', labelKey: 'profile.targetLevel_1a' },
  { value: '1b', labelKey: 'profile.targetLevel_1b' },
  { value: '2a', labelKey: 'profile.targetLevel_2a' },
  { value: '2b', labelKey: 'profile.targetLevel_2b' },
  { value: '3a', labelKey: 'profile.targetLevel_3a' },
  { value: '3b', labelKey: 'profile.targetLevel_3b' },
] as const

interface ProfileData {
  user?: {
    name: string
    email: string
    avatarUrl?: string
    levelKey: string
    targetLevelKey?: string
    joinDate: string
    bio?: { zh?: string; en?: string }
  }
  model?: {
    appId?: string
    modelName: string
    apiUrl: string
    apiKey?: string
    apiKeyMasked?: string
    apiSecret?: string
    apiSecretMasked?: string
    apiPassword?: string
    apiPasswordMasked?: string
    tokensTotal: number
    tokensUsed: number
    tokensRemaining: number
    memberExpire: string
    memberLevel?: { zh?: string; en?: string }
  }
  tokenUsage?: { date: string; input: number; output: number }[]
}

interface CoreFeatureStat {
  id: string
  completed?: number
  total?: number
  count?: number
  browsed?: number
  lastUsed?: string
  trend?: number[]
}

interface PscPartStat {
  id: string
  examCount: number
  avgScore: number
  lastDate: string
}

interface StatsData {
  tokenUsage?: { date: string; input: number; output: number }[]
  recentExams?: { date: string; type: string; score: number; totalQuestions: number }[]
  coreFeaturesStats?: CoreFeatureStat[]
  pscPartsStats?: PscPartStat[]
  practiceByType?: { type: string; count: number; label?: { zh?: string; en?: string }; accuracy?: number; trend?: number[] }[]
  scoreTrend?: { date: string; score: number }[]
  scoreTrendByPart?: {
    date: string
    dateObj?: Date
    singleCharacterReading: number
    wordReading: number
    choiceJudgment: number
    passageReading: number
    topicSpeaking: number
  }[]
  dailyPractice?: { day: string; count: number }[]
  contributionCalendar?: { date: string; count: number }[]
}

const { locale } = useI18n()
const isDark = useDark()
const profile = ref<ProfileData | null>(null)
const stats = ref<StatsData | null>(null)

// 可编辑字段：姓名、邮箱
const editingName = ref(false)
const editingEmail = ref(false)
const editNameValue = ref('')
const editEmailValue = ref('')
const nameInputRef = ref<InstanceType<typeof Input> | null>(null)
const emailInputRef = ref<InstanceType<typeof Input> | null>(null)

const targetLevelKey = computed({
  get: () => profile.value?.user?.targetLevelKey ?? '2a',
  set: (v: string) => {
    if (profile.value?.user) profile.value.user.targetLevelKey = v
  },
})

function startEditName() {
  editNameValue.value = profile.value?.user?.name ?? ''
  editingName.value = true
  nextTick(() => (nameInputRef.value?.$el as HTMLInputElement | undefined)?.focus())
}

function saveName() {
  const v = editNameValue.value.trim()
  if (profile.value?.user) profile.value.user.name = v || profile.value.user.name
  editingName.value = false
}

function cancelEditName() {
  editNameValue.value = profile.value?.user?.name ?? ''
  editingName.value = false
}

function startEditEmail() {
  editEmailValue.value = profile.value?.user?.email ?? ''
  editingEmail.value = true
  nextTick(() => (emailInputRef.value?.$el as HTMLInputElement | undefined)?.focus())
}

function saveEmail() {
  const v = editEmailValue.value.trim()
  if (profile.value?.user) profile.value.user.email = v || profile.value.user.email
  editingEmail.value = false
}

function cancelEditEmail() {
  editEmailValue.value = profile.value?.user?.email ?? ''
  editingEmail.value = false
}

const hasMember = computed(() => !!(profile.value?.model?.memberLevel && profile.value?.model?.memberExpire))

const resolvedMemberLevel = computed(() =>
  profile.value?.model?.memberLevel ? resolveI18n(profile.value.model.memberLevel, locale.value) : '—'
)

const tokenBarData = computed(() => {
  const raw = profile.value?.tokenUsage ?? stats.value?.tokenUsage ?? []
  return raw.map((d) => ({ ...d, dateObj: new Date(d.date) }))
})
const tokenUsedThisWeek = computed(() => {
  const data = tokenBarData.value
  if (!data.length) return 0
  const sorted = [...data].sort((a, b) => a.dateObj.getTime() - b.dateObj.getTime())
  const last7 = sorted.slice(-7)
  return last7.reduce((sum, d) => sum + d.input + d.output, 0)
})
const tokenUsagePercent = computed(() => {
  const total = profile.value?.model?.tokensTotal ?? 0
  const used = profile.value?.model?.tokensUsed ?? 0
  if (!total) return 0
  return Math.min(100, (used / total) * 100)
})
const tokenUsageTotalInput = computed(() => tokenBarData.value.reduce((sum, d) => sum + d.input, 0))
const tokenUsageTotalOutput = computed(() => tokenBarData.value.reduce((sum, d) => sum + d.output, 0))
const tokenUsageAvg7d = computed(() => {
  const used = tokenUsedThisWeek.value
  if (!used) return '—'
  return Math.round(used / 7).toLocaleString()
})
const tokenBarX = (d: { dateObj: Date }) => d.dateObj
const tokenBarY = [(d: { input: number }) => d.input, (d: { output: number }) => d.output]
const tokenBarColor = (_: unknown, i: number) => (i === 0 ? 'hsl(var(--primary))' : 'hsl(var(--primary) / 0.7)')
const tokenBarTooltipTemplate = (d: { date: string; input: number; output: number } | undefined) => {
  if (!d) return ''
  const dateStr = new Date(d.date).toLocaleDateString(locale.value === 'zh' ? 'zh-CN' : 'en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
  return `<div class="rounded-md border bg-popover px-3 py-2 text-sm shadow-md">
    <div class="font-medium mb-1">${dateStr}</div>
    <div class="flex justify-between gap-4 text-muted-foreground">
      <span>${locale.value === 'zh' ? '输入' : 'Input'}: ${d.input.toLocaleString()}</span>
      <span>${locale.value === 'zh' ? '输出' : 'Output'}: ${d.output.toLocaleString()}</span>
    </div>
  </div>`
}
const tokenBarCrosshairColor = (_: unknown, i: number) =>
  i === 0 ? 'hsl(var(--primary))' : 'hsl(var(--primary) / 0.7)'

const scoreTrendData = computed(() => {
  const list = stats.value?.scoreTrend ?? []
  const year = new Date().getFullYear()
  return list
    .map((d) => {
      const [month, day] = d.date.split('-').map(Number)
      const dateObj = new Date(year, month - 1, day)
      return { ...d, dateObj, score: d.score }
    })
    .sort((a, b) => a.dateObj.getTime() - b.dateObj.getTime())
})
const scoreTrendX = (d: { dateObj: Date }) => d.dateObj
const scoreTrendY = (d: { score: number }) => d.score
const scoreTrendSelectedColor = 'hsl(var(--primary))'
const scoreTrendTooltipTemplate = (d: { date: string; dateObj?: Date; score: number } | undefined) => {
  if (!d) return ''
  const dateStr = d.dateObj
    ? d.dateObj.toLocaleDateString(locale.value === 'zh' ? 'zh-CN' : 'en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    : d.date
  const scoreLabel = locale.value === 'zh' ? '得分' : 'Score'
  return `<div class="rounded-md border bg-popover px-3 py-2 text-sm shadow-md">
    <div class="font-medium mb-1">${dateStr}</div>
    <div class="flex justify-between gap-4"><span class="text-muted-foreground">${scoreLabel}</span><span class="font-medium">${d.score}</span></div>
  </div>`
}
const scoreTrendSvgDefs = `
  <linearGradient id="fillScoreSelected" x1="0" y1="0" x2="0" y2="1">
    <stop offset="5%" stop-color="hsl(var(--primary))" stop-opacity="0.8" />
    <stop offset="95%" stop-color="hsl(var(--primary))" stop-opacity="0.1" />
  </linearGradient>
`

const coreFeaturesWithLabel = computed(() => {
  const list = stats.value?.coreFeaturesStats ?? []
  return list.map((item) => ({
    ...item,
    name: item.id ? (locale.value === 'zh' ? getCoreFeatureNameZh(item.id) : getCoreFeatureNameEn(item.id)) : item.id,
  }))
})

function getCoreFeatureNameZh(id: string): string {
  const map: Record<string, string> = {
    mockExam: 'PSC 模拟考试',
    personalizedPractice: '专项训练',
    errorNotebook: '错题本',
    questionBank: 'PSC考试题库',
  }
  return map[id] ?? id
}

function getCoreFeatureNameEn(id: string): string {
  const map: Record<string, string> = {
    mockExam: 'PSC Mock Exam',
    personalizedPractice: 'Specialized Training',
    errorNotebook: 'Error Notebook',
    questionBank: 'PSC Exam Question Bank',
  }
  return map[id] ?? id
}

const pscPartsWithLabel = computed(() => {
  const list = stats.value?.pscPartsStats ?? []
  return list.map((item) => ({
    ...item,
    name: item.id ? (locale.value === 'zh' ? getPscPartNameZh(item.id) : getPscPartNameEn(item.id)) : item.id,
  }))
})

function getPscPartNameZh(id: string): string {
  const map: Record<string, string> = {
    singleCharacterReading: '读单音节字词',
    wordReading: '读多音节词语',
    choiceJudgment: '选择判断',
    passageReading: '朗读短文',
    topicSpeaking: '命题说话',
  }
  return map[id] ?? id
}

function getPscPartNameEn(id: string): string {
  const map: Record<string, string> = {
    singleCharacterReading: 'Single Character Reading',
    wordReading: 'Multi-syllable Word Reading',
    choiceJudgment: 'Choice & Judgment',
    passageReading: 'Passage Reading',
    topicSpeaking: 'Topic Speaking',
  }
  return map[id] ?? id
}

const practiceByTypeWithLabel = computed(() => {
  const list = stats.value?.practiceByType ?? []
  return list.map((item) => ({
    ...item,
    label: item.label ? resolveI18n(item.label, locale.value) : item.type,
  }))
})

function sparkHeight(value: number, arr?: number[]): number {
  if (!arr?.length) return 0
  const max = Math.max(...arr, 1)
  return Math.round((value / max) * 100)
}

const dailyData = computed(() => stats.value?.dailyPractice ?? [])

// 贡献热力图：vue3-calendar-heatmap（GitHub 风格）
const selectedContributionYear = ref(String(new Date().getFullYear()))
const contributionYearOptions = computed(() => {
  const y = new Date().getFullYear()
  return [y + 1, y, y - 1, y - 2, y - 3, y - 4, y - 5]
})

const contributionHeatmapValues = computed(() => {
  const year = parseInt(selectedContributionYear.value, 10)
  const list = stats.value?.contributionCalendar ?? []
  return list
    .filter(({ date }) => date.startsWith(String(year)))
    .map(({ date, count }) => ({ date, count }))
})

const contributionEndDate = computed(
  () => `${selectedContributionYear.value}-12-31`
)

const contributionRangeColor = computed(() =>
  isDark.value
    ? ['hsl(var(--muted))', 'hsl(var(--primary) / 0.2)', 'hsl(var(--primary) / 0.4)', 'hsl(var(--primary) / 0.6)', 'hsl(var(--primary) / 0.8)', 'hsl(var(--primary))']
    : ['hsl(var(--muted))', 'hsl(var(--primary) / 0.2)', 'hsl(var(--primary) / 0.4)', 'hsl(var(--primary) / 0.6)', 'hsl(var(--primary) / 0.8)', 'hsl(var(--primary))']
)

function contributionTooltipFormatter(v: { date: Date | string; count: number }): string {
  const dateStr = typeof v.date === 'string' ? v.date : new Date(v.date).toISOString().slice(0, 10)
  return locale.value === 'zh'
    ? `${dateStr}${v.count > 0 ? `: ${v.count} 次` : ''}`
    : `${dateStr}${v.count > 0 ? `: ${v.count} contributions` : ''}`
}

const totalContributions = computed(() => {
  const year = parseInt(selectedContributionYear.value, 10)
  const list = stats.value?.contributionCalendar ?? []
  return list.filter(({ date }) => date.startsWith(String(year))).reduce((sum, { count }) => sum + count, 0)
})

onMounted(async () => {
  try {
    const [pRes, sRes] = await Promise.all([
      fetch('/data/profile.json'),
      fetch('/data/stats.json'),
    ])
    if (pRes.ok) profile.value = await pRes.json()
    if (sRes.ok) stats.value = await sRes.json()
  } catch (_) {
    // fallback
  }
})
</script>

<style scoped>
.contribution-heatmap-wrapper :deep(.vch__legend) {
  color: hsl(var(--muted-foreground));
}
.contribution-heatmap-wrapper :deep(svg.vch__wrapper text) {
  fill: hsl(var(--muted-foreground));
}
</style>
