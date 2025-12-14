import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Компоненты страниц (создадим позже)
import HomePage from '../views/HomePage.vue'
import CarsPage from '../views/CarsPage.vue'
import CarDetailPage from '../views/CarDetailPage.vue'
import LoginPage from '../views/LoginPage.vue'
import ProfilePage from '../views/ProfilePage.vue'
import RequestsPage from '../views/RequestsPage.vue'
import AboutPage from '../views/AboutPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
    meta: { title: 'Главная' }
  },
  {
    path: '/cars',
    name: 'cars',
    component: CarsPage,
    meta: { title: 'Автомобили' }
  },
  {
    path: '/cars/:id',
    name: 'car-detail',
    component: CarDetailPage,
    meta: { title: 'Детали автомобиля' }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
    meta: { title: 'Вход', guestOnly: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage,
    meta: { title: 'Профиль', requiresAuth: true }
  },
  {
    path: '/requests',
    name: 'requests',
    component: RequestsPage,
    meta: { title: 'Мои заявки', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard для проверки аутентификации
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Устанавливаем заголовок страницы
  document.title = to.meta.title ? `${to.meta.title} | AutoElite` : 'AutoElite'

  // Проверка на необходимость аутентификации
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
    return
  }

  // Проверка на guest-only страницы (только для неавторизованных)
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }

  next()
})

export default router