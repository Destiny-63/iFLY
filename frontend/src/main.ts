import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)

// 将 i18n 实例挂载到 window，供 useSettings 使用
;(window as any).__VUE_I18N__ = i18n

app.mount('#app')
