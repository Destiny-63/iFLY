import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

export type FontSize = 'small' | 'medium' | 'large'
export type Language = 'zh' | 'en' | 'fr' | 'it' | 'es' | 'ar'
export type Theme =
  | 'default'
  | 'red'
  | 'rose'
  | 'orange'
  | 'green'
  | 'blue'
  | 'yellow'
  | 'violet'

interface SettingsState {
  fontSize: FontSize
  language: Language
  theme: Theme
}

const STORAGE_KEY = 'ifly-ui-settings'

const baseThemeVars = {
  background: '0 0% 100%',
  foreground: '222.2 84% 4.9%',
  card: '0 0% 100%',
  'card-foreground': '222.2 84% 4.9%',
  popover: '0 0% 100%',
  'popover-foreground': '222.2 84% 4.9%',
  primary: '222.2 47.4% 11.2%',
  'primary-foreground': '210 40% 98%',
  secondary: '210 40% 96.1%',
  'secondary-foreground': '222.2 47.4% 11.2%',
  muted: '210 40% 96.1%',
  'muted-foreground': '215.4 16.3% 46.9%',
  accent: '210 40% 96.1%',
  'accent-foreground': '222.2 47.4% 11.2%',
  destructive: '0 84.2% 60.2%',
  'destructive-foreground': '210 40% 98%',
  border: '214.3 31.8% 91.4%',
  input: '214.3 31.8% 91.4%',
  ring: '222.2 84% 4.9%',
  'sidebar-background': '0 0% 98%',
  'sidebar-foreground': '240 5.3% 26.1%',
  'sidebar-primary': '240 5.9% 10%',
  'sidebar-primary-foreground': '0 0% 98%',
  'sidebar-accent': '240 4.8% 95.9%',
  'sidebar-accent-foreground': '240 5.9% 10%',
  'sidebar-border': '220 13% 91%',
  'sidebar-ring': '217.2 91.2% 59.8%',
}

// 主题现在通过 CSS 类应用，不再需要 themeOverrides
const themeOverrides: Record<Theme, Partial<typeof baseThemeVars>> = {
  default: {},
  red: {},
  rose: {},
  orange: {},
  green: {},
  blue: {},
  yellow: {},
  violet: {},
}

const defaultSettings: SettingsState = {
  fontSize: 'medium',
  language: 'zh',
  theme: 'default',
}

const settingsRef = ref<SettingsState>(defaultSettings)
let initialized = false

function applyFontSize(size: FontSize) {
  const map = { small: '14px', medium: '16px', large: '18px' } as const
  document.documentElement.style.fontSize = map[size]
}

function applyTheme(theme: Theme) {
  const root = document.documentElement
  // 移除所有主题类
  const allThemes = ['theme-red', 'theme-rose', 'theme-orange', 'theme-green', 'theme-blue', 'theme-yellow', 'theme-violet']
  allThemes.forEach(themeClass => root.classList.remove(themeClass))
  
  // 应用新主题类（default 不需要类）
  if (theme !== 'default') {
    root.classList.add(`theme-${theme}`)
  }
  
  // 确保 CSS 变量立即更新
  // 通过读取计算样式来强制浏览器重新计算
  void root.offsetHeight
}

function applyLanguage(language: Language, i18nInstance?: any) {
  document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en'
  // 同步到 i18n
  if (i18nInstance) {
    i18nInstance.global.locale.value = language
  }
}

function loadFromStorage(): SettingsState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return defaultSettings
    return { ...defaultSettings, ...JSON.parse(raw) }
  } catch {
    return defaultSettings
  }
}

export function useSettings() {
  if (!initialized && typeof window !== 'undefined') {
    settingsRef.value = loadFromStorage()
    applyFontSize(settingsRef.value.fontSize)
    applyTheme(settingsRef.value.theme)
    
    // 初始化时同步语言到 i18n
    const i18n = (window as any).__VUE_I18N__
    if (i18n) {
      i18n.global.locale.value = settingsRef.value.language
    }
    applyLanguage(settingsRef.value.language)

    watch(
      settingsRef,
      (next) => {
        applyFontSize(next.fontSize)
        applyTheme(next.theme)
        
        // 同步语言到 i18n
        const i18n = (window as any).__VUE_I18N__
        if (i18n) {
          i18n.global.locale.value = next.language
        }
        applyLanguage(next.language)
        localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
      },
      { deep: true }
    )
    initialized = true
  }

  const updateSettings = (updates: Partial<SettingsState>) => {
    settingsRef.value = { ...settingsRef.value, ...updates }
  }

  return {
    settings: settingsRef,
    updateSettings,
  }
}

