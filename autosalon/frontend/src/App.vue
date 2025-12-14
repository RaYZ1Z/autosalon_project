<template>
  <div id="app">
    <!-- Навигация -->
    <nav class="navbar">
      <div class="container">
        <router-link to="/" class="navbar-brand">🚗 AutoElite</router-link>
        <div class="navbar-menu">
          <router-link to="/">🏠 Главная</router-link>
          <router-link to="/cars">🚗 Автомобили</router-link>
          <router-link to="/profile" v-if="isAuthenticated">👤 Профиль</router-link>
          <router-link to="/login" v-else>🔑 Войти</router-link>
          <router-link to="/requests" v-if="isAuthenticated">📋 Мои заявки</router-link>
        </div>
      </div>
    </nav>

    <!-- Основной контент -->
    <main class="main-content">
      <div class="container">
        <router-view />
      </div>
    </main>

    <!-- Футер -->
    <footer class="footer">
      <div class="container">
        <p>© 2024 AutoElite. Все права защищены.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from './stores/auth'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore()

    return {
      isAuthenticated: computed(() => authStore.isAuthenticated)
    }
  }
}
</script>

<style>
/* Базовые стили */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8f9fa;
  color: #333;
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Навигация */
.navbar {
  background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
  color: white;
  padding: 15px 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.navbar .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: white;
}

.navbar-menu {
  display: flex;
  gap: 20px;
}

.navbar-menu a {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.navbar-menu a:hover {
  background-color: rgba(255,255,255,0.1);
}

.navbar-menu a.router-link-active {
  background-color: rgba(255,255,255,0.2);
}

/* Основной контент */
.main-content {
  min-height: calc(100vh - 140px);
  padding: 30px 0;
}

/* Футер */
.footer {
  background: #333;
  color: white;
  padding: 20px 0;
  text-align: center;
}
</style>