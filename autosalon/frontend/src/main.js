import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Создаём приложение
const app = createApp(App)

// Используем Pinia для состояния
const pinia = createPinia()
app.use(pinia)

// Используем Vue Router
app.use(router)

// Монтируем приложение
app.mount('#app')