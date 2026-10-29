<template>
  <SidebarProvider>
    <Sidebar />

    <SidebarInset>
      <header class="flex h-14 items-center gap-2 border-b bg-card px-4">
        <SidebarTrigger />
        <div class="text-sm font-medium">{{ $t('about.title') }}</div>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="mx-auto max-w-3xl space-y-6">
          <div>
            <h1 class="text-2xl font-bold tracking-tight">{{ $t('about.title') }}</h1>
            <p class="mt-1 text-sm text-muted-foreground">{{ $t('about.subtitle') }}</p>
          </div>

          <!-- 模型配置 -->
          <Card class="overflow-hidden">
            <CardHeader class="pb-2">
              <CardTitle class="text-base font-semibold">{{ $t('profile.modelConfig') }}</CardTitle>
              <CardDescription class="text-sm text-muted-foreground">{{ $t('profile.modelAndTokenDesc') }}</CardDescription>
            </CardHeader>
            <CardContent>
              <div class="grid gap-4 sm:grid-cols-2">
                <Field>
                  <FieldLabel class="text-sm">{{ $t('profile.appId') }}</FieldLabel>
                  <FieldContent>
                    <Input v-model="appIdValue" class="h-9 text-sm font-mono" placeholder="your_app_id" @blur="saveAppId" />
                  </FieldContent>
                </Field>
                <Field>
                  <FieldLabel class="text-sm">{{ $t('profile.model') }}</FieldLabel>
                  <FieldContent>
                    <Input v-model="modelNameValue" class="h-9 text-sm font-mono" placeholder="spark-x" @blur="saveModelName" />
                  </FieldContent>
                </Field>
                <Field class="sm:col-span-2">
                  <FieldLabel class="text-sm">{{ $t('profile.apiUrl') }}</FieldLabel>
                  <FieldContent>
                    <Input v-model="apiUrlValue" class="h-9 text-sm font-mono" placeholder="https://spark-api-open.xf-yun.com/v2" @blur="saveApiUrl" />
                  </FieldContent>
                </Field>
                <Field>
                  <FieldLabel class="text-sm">{{ $t('profile.apiKey') }}</FieldLabel>
                  <FieldContent>
                    <div class="relative">
                      <Input
                        v-model="apiKeyValue"
                        :type="showApiKey ? 'text' : 'password'"
                        class="h-9 pr-9 text-sm font-mono"
                        placeholder="••••••••••••"
                        autocomplete="off"
                        @blur="saveApiKey"
                      />
                      <button
                        type="button"
                        class="absolute right-2 top-1/2 -translate-y-1/2 rounded p-1 text-muted-foreground hover:bg-muted hover:text-foreground"
                        :aria-label="showApiKey ? $t('profile.hideSecret') : $t('profile.showSecret')"
                        @click="showApiKey = !showApiKey"
                      >
                        <EyeOff v-if="showApiKey" class="size-4" />
                        <Eye v-else class="size-4" />
                      </button>
                    </div>
                  </FieldContent>
                </Field>
                <Field>
                  <FieldLabel class="text-sm">{{ $t('profile.apiSecret') }}</FieldLabel>
                  <FieldContent>
                    <div class="relative">
                      <Input
                        v-model="apiSecretValue"
                        :type="showApiSecret ? 'text' : 'password'"
                        class="h-9 pr-9 text-sm font-mono"
                        placeholder="••••••••••••"
                        autocomplete="off"
                        @blur="saveApiSecret"
                      />
                      <button
                        type="button"
                        class="absolute right-2 top-1/2 -translate-y-1/2 rounded p-1 text-muted-foreground hover:bg-muted hover:text-foreground"
                        :aria-label="showApiSecret ? $t('profile.hideSecret') : $t('profile.showSecret')"
                        @click="showApiSecret = !showApiSecret"
                      >
                        <EyeOff v-if="showApiSecret" class="size-4" />
                        <Eye v-else class="size-4" />
                      </button>
                    </div>
                  </FieldContent>
                </Field>
                <Field>
                  <FieldLabel class="text-sm">{{ $t('profile.apiPassword') }}</FieldLabel>
                  <FieldContent>
                    <div class="relative">
                      <Input
                        v-model="apiPasswordValue"
                        :type="showApiPassword ? 'text' : 'password'"
                        class="h-9 pr-9 text-sm font-mono"
                        placeholder="••••••••••••"
                        autocomplete="off"
                        @blur="saveApiPassword"
                      />
                      <button
                        type="button"
                        class="absolute right-2 top-1/2 -translate-y-1/2 rounded p-1 text-muted-foreground hover:bg-muted hover:text-foreground"
                        :aria-label="showApiPassword ? $t('profile.hideSecret') : $t('profile.showSecret')"
                        @click="showApiPassword = !showApiPassword"
                      >
                        <EyeOff v-if="showApiPassword" class="size-4" />
                        <Eye v-else class="size-4" />
                      </button>
                    </div>
                  </FieldContent>
                </Field>
              </div>
            </CardContent>
          </Card>

          <!-- 开发者信息 -->
          <Card class="overflow-hidden">
            <CardHeader class="pb-2">
              <CardTitle class="text-base font-semibold">{{ $t('about.developerInfo') }}</CardTitle>
              <CardDescription class="text-sm text-muted-foreground">{{ $t('about.developerInfoDesc') }}</CardDescription>
            </CardHeader>
            <CardContent class="space-y-4">
              <div class="grid gap-4 text-sm sm:grid-cols-2">
                <div>
                  <p class="text-xs text-muted-foreground">{{ $t('about.appName') }}</p>
                  <p class="font-medium">{{ $t('common.appName') }}</p>
                </div>
                <div>
                  <p class="text-xs text-muted-foreground">{{ $t('about.version') }}</p>
                  <p class="font-medium">1.0.0</p>
                </div>
                <div>
                  <p class="text-xs text-muted-foreground">{{ $t('about.techStack') }}</p>
                  <p class="font-medium">Vue 3 · Vite · TypeScript</p>
                </div>
                <div>
                  <p class="text-xs text-muted-foreground">{{ $t('about.contact') }}</p>
                  <p class="font-medium">demo@iflytek.com</p>
                </div>
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
import Sidebar from '@/components/Sidebar.vue'
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Field, FieldLabel, FieldContent } from '@/components/ui/field'
import { Eye, EyeOff } from 'lucide-vue-next'

interface ProfileData {
  model?: {
    appId?: string
    modelName: string
    apiUrl: string
    apiKey?: string
    apiSecret?: string
    apiPassword?: string
  }
}

const profile = ref<ProfileData | null>(null)
const showApiKey = ref(false)
const showApiSecret = ref(false)
const showApiPassword = ref(false)

const appIdValue = computed({
  get: () => profile.value?.model?.appId ?? '',
  set: (v: string) => {
    if (profile.value?.model) profile.value.model.appId = v
  },
})
const modelNameValue = computed({
  get: () => profile.value?.model?.modelName ?? '',
  set: (v: string) => {
    if (profile.value?.model) profile.value.model.modelName = v
  },
})
const apiUrlValue = computed({
  get: () => profile.value?.model?.apiUrl ?? '',
  set: (v: string) => {
    if (profile.value?.model) profile.value.model.apiUrl = v
  },
})
const apiKeyValue = computed({
  get: () => profile.value?.model?.apiKey ?? '',
  set: (v: string) => {
    if (profile.value?.model) profile.value.model.apiKey = v
  },
})
const apiSecretValue = computed({
  get: () => profile.value?.model?.apiSecret ?? '',
  set: (v: string) => {
    if (profile.value?.model) profile.value.model.apiSecret = v
  },
})
const apiPasswordValue = computed({
  get: () => profile.value?.model?.apiPassword ?? '',
  set: (v: string) => {
    if (profile.value?.model) profile.value.model.apiPassword = v
  },
})

function saveAppId() {
  const v = appIdValue.value.trim()
  if (profile.value?.model) profile.value.model.appId = v || profile.value.model.appId
}
function saveModelName() {
  const v = modelNameValue.value.trim()
  if (profile.value?.model) profile.value.model.modelName = v || profile.value.model.modelName
}
function saveApiUrl() {
  const v = apiUrlValue.value.trim()
  if (profile.value?.model) profile.value.model.apiUrl = v || profile.value.model.apiUrl
}
function saveApiKey() {
  const v = apiKeyValue.value
  if (profile.value?.model) profile.value.model.apiKey = v
}
function saveApiSecret() {
  const v = apiSecretValue.value
  if (profile.value?.model) profile.value.model.apiSecret = v
}
function saveApiPassword() {
  const v = apiPasswordValue.value
  if (profile.value?.model) profile.value.model.apiPassword = v
}

onMounted(async () => {
  try {
    const res = await fetch('/data/profile.json')
    if (res.ok) profile.value = await res.json()
  } catch (_) {
    // fallback
  }
})
</script>
