import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // Состояние
  const user = ref(null)
  const token = ref(localStorage.getItem('autosalon_token') || null)

  // Геттеры
  const isAuthenticated = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role || 'client')

  // Действия
  function setUser(userData) {
    user.value = userData
  }

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('autosalon_token', newToken)
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('autosalon_token')
  }

  // Проверка ролей
  function isManager() {
    return userRole.value === 'manager' || userRole.value === 'admin'
  }

  function isAdmin() {
    return userRole.value === 'admin'
  }

  return {
    // Состояние
    user,
    token,

    // Геттеры
    isAuthenticated,
    userRole,

    // Действия
    setUser,
    setToken,
    logout,
    isManager,
    isAdmin
  }
})