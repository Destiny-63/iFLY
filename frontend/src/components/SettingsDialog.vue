<template>
  <Dialog :open="open" @update:open="emit('update:open', $event)">
    <DialogContent class="sm:max-w-[680px] max-h-[85vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle class="text-xl font-bold">{{ $t('settings.title') }}</DialogTitle>
        <DialogDescription class="text-sm text-muted-foreground">
          {{ $t('settings.description') }}
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-6 py-4">
        <!-- 文字大小设置 -->
        <div class="space-y-3">
          <Label class="text-sm font-semibold">{{ $t('settings.fontSize') }}</Label>
          <Select :model-value="local.fontSize" @update:model-value="local.fontSize = $event as FontSize">
            <SelectTrigger>
              <SelectValue>
                <span>{{ fontSizeLabels[local.fontSize] || '' }}</span>
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="size in fontSizeOptions" :key="size.value" :value="size.value">
                <div class="flex items-center gap-2">
                  <span :class="['font-semibold', size.class]">Aa</span>
                  <span>{{ size.label }}</span>
                  <span class="text-xs text-muted-foreground">({{ size.px }})</span>
                </div>
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        <Separator />

        <!-- 界面语言设置 -->
        <div class="space-y-3">
          <Label class="text-sm font-semibold">{{ $t('settings.language') }}</Label>
          <Select :model-value="local.language" @update:model-value="local.language = $event as Language">
            <SelectTrigger>
              <SelectValue>
                <span>{{ languageLabels[local.language] || '' }}</span>
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="lang in languageOptions" :key="lang.value" :value="lang.value">
                <div class="flex items-center gap-2">
                  <span>{{ lang.label }}</span>
                  <span class="text-xs text-muted-foreground">({{ lang.desc }})</span>
                </div>
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        <Separator />

        <!-- 主题色系设置 -->
        <div class="space-y-3">
          <Label class="text-sm font-semibold">{{ $t('settings.theme') }}</Label>
          <Select :model-value="local.theme" @update:model-value="local.theme = $event as Theme">
            <SelectTrigger>
              <SelectValue>
                <div class="flex items-center gap-2">
                  <div
                    class="size-4 rounded-full border border-border/50 shrink-0"
                    :style="{ backgroundColor: `hsl(${getThemeColor(local.theme, 'primary')})` }"
                  />
                  <span>{{ themeLabels[local.theme] || '' }}</span>
                </div>
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="theme in themeOptions" :key="theme.value" :value="theme.value">
                <div class="flex items-center gap-2">
                  <div
                    class="size-4 rounded-full border border-border/50 shrink-0"
                    :style="{ backgroundColor: `hsl(${getThemeColor(theme.value, 'primary')})` }"
                  />
                  <span>{{ theme.label }}</span>
                </div>
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <DialogFooter class="gap-2">
        <Button variant="outline" @click="handleCancel">{{ $t('settings.cancel') }}</Button>
        <Button @click="save">{{ $t('settings.save') }}</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import { Check } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useSettings, type FontSize, type Language, type Theme } from '@/composables/useSettings'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Props {
  open: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{ 'update:open': [value: boolean] }>()

const { settings, updateSettings } = useSettings()

const local = reactive({
  fontSize: settings.value.fontSize as FontSize,
  language: settings.value.language as Language,
  theme: settings.value.theme as Theme,
})

watch(
  () => props.open,
  (v) => {
    if (v) {
      local.fontSize = settings.value.fontSize
      local.language = settings.value.language
      local.theme = settings.value.theme
    }
  }
)

// 实时预览主题（直接应用，保存时确认）
watch(
  () => local.theme,
  (newTheme) => {
    if (props.open) {
      // 实时应用主题预览
      const root = document.documentElement
      const allThemes = ['theme-red', 'theme-rose', 'theme-orange', 'theme-green', 'theme-blue', 'theme-yellow', 'theme-violet']
      allThemes.forEach(themeClass => root.classList.remove(themeClass))
      
      if (newTheme !== 'default') {
        root.classList.add(`theme-${newTheme}`)
      }
      
      // 强制浏览器重新计算 CSS 变量
      void root.offsetHeight
    }
  }
)

const fontSizeOptions = computed(() => {
  try {
    return [
      { value: 'small' as FontSize, label: t('settings.small'), px: '14px', class: 'text-base' },
      { value: 'medium' as FontSize, label: t('settings.medium'), px: '16px', class: 'text-lg' },
      { value: 'large' as FontSize, label: t('settings.large'), px: '18px', class: 'text-xl' },
    ]
  } catch {
    return [
      { value: 'small' as FontSize, label: '小', px: '14px', class: 'text-base' },
      { value: 'medium' as FontSize, label: '中', px: '16px', class: 'text-lg' },
      { value: 'large' as FontSize, label: '大', px: '18px', class: 'text-xl' },
    ]
  }
})

const languageOptions = computed(() => {
  try {
    return [
      { value: 'zh' as Language, label: t('settings.chinese'), desc: t('settings.chineseDesc') },
      { value: 'en' as Language, label: t('settings.english'), desc: t('settings.englishDesc') },
      { value: 'fr' as Language, label: t('settings.french'), desc: t('settings.frenchDesc') },
      { value: 'it' as Language, label: t('settings.italian'), desc: t('settings.italianDesc') },
      { value: 'es' as Language, label: t('settings.spanish'), desc: t('settings.spanishDesc') },
      { value: 'ar' as Language, label: t('settings.arabic'), desc: t('settings.arabicDesc') },
    ]
  } catch {
    return [
      { value: 'zh' as Language, label: '中文', desc: '简体中文界面' },
      { value: 'en' as Language, label: 'English', desc: 'English interface' },
      { value: 'fr' as Language, label: 'Français', desc: 'Interface française' },
      { value: 'it' as Language, label: 'Italiano', desc: 'Interfaccia italiana' },
      { value: 'es' as Language, label: 'Español', desc: 'Interfaz en español' },
      { value: 'ar' as Language, label: 'العربية', desc: 'واجهة عربية' },
    ]
  }
})

const themeOptions = computed(() => {
  try {
    return [
      { value: 'default' as Theme, label: t('settings.default') },
      { value: 'red' as Theme, label: t('settings.red') },
      { value: 'rose' as Theme, label: t('settings.rose') },
      { value: 'orange' as Theme, label: t('settings.orange') },
      { value: 'green' as Theme, label: t('settings.green') },
      { value: 'blue' as Theme, label: t('settings.blue') },
      { value: 'yellow' as Theme, label: t('settings.yellow') },
      { value: 'violet' as Theme, label: t('settings.violet') },
    ]
  } catch {
    return [
      { value: 'default' as Theme, label: '默认' },
      { value: 'red' as Theme, label: '红色' },
      { value: 'rose' as Theme, label: '玫瑰' },
      { value: 'orange' as Theme, label: '橙色' },
      { value: 'green' as Theme, label: '绿色' },
      { value: 'blue' as Theme, label: '蓝色' },
      { value: 'yellow' as Theme, label: '黄色' },
      { value: 'violet' as Theme, label: '紫色' },
    ]
  }
})

const fontSizeLabels = computed(() => {
  try {
    return {
      small: `${t('settings.small')}（14px）`,
      medium: `${t('settings.medium')}（16px）`,
      large: `${t('settings.large')}（18px）`,
    }
  } catch {
    return {
      small: '小（14px）',
      medium: '中（16px）',
      large: '大（18px）',
    }
  }
})

const languageLabels = computed(() => {
  try {
    return {
      zh: t('settings.chinese'),
      en: t('settings.english'),
      fr: t('settings.french'),
      it: t('settings.italian'),
      es: t('settings.spanish'),
      ar: t('settings.arabic'),
    }
  } catch {
    return {
      zh: '中文',
      en: 'English',
      fr: 'Français',
      it: 'Italiano',
      es: 'Español',
      ar: 'العربية',
    }
  }
})

const themeLabels = computed(() => {
  try {
    return {
      default: t('settings.default'),
      red: t('settings.red'),
      rose: t('settings.rose'),
      orange: t('settings.orange'),
      green: t('settings.green'),
      blue: t('settings.blue'),
      yellow: t('settings.yellow'),
      violet: t('settings.violet'),
    }
  } catch {
    return {
      default: '默认',
      red: '红色',
      rose: '玫瑰',
      orange: '橙色',
      green: '绿色',
      blue: '蓝色',
      yellow: '黄色',
      violet: '紫色',
    }
  }
})

// 主题颜色映射（用于预览圆圈）
const themeColors: Record<Theme, Record<string, string>> = {
  default: { primary: '222.2 47.4% 11.2%' },
  red: { primary: '0 72.2% 50.6%' },
  rose: { primary: '346.8 77.2% 49.8%' },
  orange: { primary: '24.6 95% 53.1%' },
  green: { primary: '142.1 76.2% 36.3%' },
  blue: { primary: '221.2 83.2% 53.3%' },
  yellow: { primary: '47.9 95.8% 53.1%' },
  violet: { primary: '262.1 83.3% 57.8%' },
}

// 获取主题颜色的辅助函数
function getThemeColor(theme: Theme, colorKey: string): string {
  return themeColors[theme]?.[colorKey] || themeColors.default[colorKey] || '0 0% 0%'
}

const save = () => {
  // 确保使用当前 local 的值保存
  const updates = {
    fontSize: local.fontSize,
    language: local.language,
    theme: local.theme,
  }
  
  // 先应用主题，确保立即生效
  const root = document.documentElement
  const allThemes = ['theme-red', 'theme-rose', 'theme-orange', 'theme-green', 'theme-blue', 'theme-yellow', 'theme-violet']
  allThemes.forEach(themeClass => root.classList.remove(themeClass))
  
  if (updates.theme !== 'default') {
    root.classList.add(`theme-${updates.theme}`)
  }
  
  void root.offsetHeight
  
  // 然后保存设置
  updateSettings(updates)
  emit('update:open', false)
}

const handleCancel = () => {
  // 恢复原始设置和主题
  const originalTheme = settings.value.theme
  local.fontSize = settings.value.fontSize
  local.language = settings.value.language
  local.theme = originalTheme
  
  // 恢复原始主题
  const root = document.documentElement
  const allThemes = ['theme-red', 'theme-rose', 'theme-orange', 'theme-green', 'theme-blue', 'theme-yellow', 'theme-violet']
  allThemes.forEach(themeClass => root.classList.remove(themeClass))
  
  if (originalTheme !== 'default') {
    root.classList.add(`theme-${originalTheme}`)
  }
  
  void root.offsetHeight
  
  emit('update:open', false)
}
</script>

