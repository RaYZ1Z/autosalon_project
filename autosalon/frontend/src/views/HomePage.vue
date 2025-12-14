<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            <span class="gradient-text">Auto</span><span class="hero-title-accent">Elite</span>
          </h1>
          <p class="hero-subtitle">
            Премиум автомобили с доставкой по всей России
          </p>
          <div class="hero-stats">
            <div class="stat-item">
              <div class="stat-number">500+</div>
              <div class="stat-label">Автомобилей</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">98%</div>
              <div class="stat-label">Довольных клиентов</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">24/7</div>
              <div class="stat-label">Поддержка</div>
            </div>
          </div>
        </div>
        <div class="hero-actions">
          <router-link to="/vue-cars" class="btn btn-primary-main">
            <i class="fas fa-car me-2"></i>Каталог автомобилей
          </router-link>
          <router-link to="/login" class="btn btn-outline-main" v-if="!isAuthenticated">
            <i class="fas fa-sign-in-alt me-2"></i>Личный кабинет
          </router-link>
        </div>
      </div>
      <div class="hero-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Почему выбирают AutoElite</h2>
        </div>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <i class="fas fa-shield-alt feature-icon"></i>
            </div>
            <h3>Гарантия качества</h3>
            <p>Все автомобили проходят полную диагностику и имеют официальную гарантию</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <i class="fas fa-tags feature-icon"></i>
            </div>
            <h3>Лучшие цены</h3>
            <p>Конкурентные цены и выгодные условия кредитования от ведущих банков</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <i class="fas fa-tools feature-icon"></i>
            </div>
            <h3>Техническая поддержка</h3>
            <p>Круглосуточная техническая поддержка и консультации специалистов</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <i class="fas fa-truck feature-icon"></i>
            </div>
            <h3>Доставка по России</h3>
            <p>Организуем доставку автомобиля в любой регион России</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <h2>Готовы выбрать свой автомобиль?</h2>
          <p>Более 500 автомобилей в наличии. Найдите идеальный вариант для себя.</p>
          <router-link to="/vue-cars" class="btn btn-primary-main btn-large">
            <i class="fas fa-search me-2"></i>Начать поиск
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'HomePage',
  setup() {
    const authStore = useAuthStore()

    return {
      isAuthenticated: computed(() => authStore.isAuthenticated)
    }
  }
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* === HERO SECTION === */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  color: #f8fafc;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 1200px;
  padding: 0 20px;
  animation: fadeInUp 1s ease-out;
}

.hero-text {
  margin-bottom: 50px;
}

.hero-title {
  font-size: clamp(3rem, 8vw, 6rem);
  font-weight: 800;
  margin-bottom: 20px;
  line-height: 1.1;
}

.hero-title-accent {
  color: #3b82f6;
}

.hero-subtitle {
  font-size: clamp(1.2rem, 3vw, 1.8rem);
  margin-bottom: 40px;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.4;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 50px;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
  animation: fadeInUp 1s ease-out 0.3s both;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  color: #3b82f6;
  margin-bottom: 5px;
  text-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  animation: fadeInUp 1s ease-out 0.6s both;
}

.btn {
  padding: 16px 32px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  position: relative;
  overflow: hidden;
  min-width: 200px;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.btn:hover::before {
  left: 100%;
}

.btn-primary-main {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #1e1b4b;
  box-shadow: 0 8px 25px rgba(251, 191, 36, 0.3);
}

.btn-primary-main:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(251, 191, 36, 0.4);
}

.btn-outline-main {
  background: rgba(255, 255, 255, 0.1);
  color: #fbbf24;
  border: 2px solid #fbbf24;
  backdrop-filter: blur(10px);
}

.btn-outline-main:hover {
  background: #fbbf24;
  color: #1e1b4b;
  border-color: #fbbf24;
  transform: translateY(-2px);
}

.btn-large {
  padding: 20px 40px;
  font-size: 1.2rem;
  min-width: 250px;
}

/* Hero Shapes */
.hero-shapes {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 1;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 300px;
  height: 300px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 200px;
  height: 200px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 150px;
  height: 150px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

/* === FEATURES SECTION === */
.features-section {
  padding: 100px 0;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
  position: relative;
}

.section-header {
  text-align: center;
  margin-bottom: 80px;
}

.section-title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 700;
  color: #f8fafc;
  margin-bottom: 20px;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #fbbf24, #f59e0b);
  border-radius: 2px;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #cbd5e1;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 40px 30px;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #fbbf24, #f59e0b, #ec4899);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  background: rgba(255, 255, 255, 0.08);
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 25px;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(251, 191, 36, 0.3);
  transition: all 0.3s ease;
}

.feature-card:hover .feature-icon-wrapper {
  transform: scale(1.1);
  box-shadow: 0 12px 35px rgba(251, 191, 36, 0.4);
}

.feature-icon {
  font-size: 2rem;
  color: #1e1b4b;
}

.feature-card h3 {
  color: #f8fafc;
  margin-bottom: 15px;
  font-size: 1.4rem;
  font-weight: 600;
}

.feature-card p {
  color: #cbd5e1;
  line-height: 1.6;
  margin: 0;
}

/* === CTA SECTION === */
.cta-section {
  padding: 80px 0;
  background: linear-gradient(135deg, #1a56db, #3b82f6);
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
  animation: backgroundMove 20s linear infinite;
}

.cta-content {
  text-align: center;
  color: white;
  max-width: 600px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.cta-content h2 {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 700;
  margin-bottom: 20px;
}

.cta-content p {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
  line-height: 1.6;
}

/* === ANIMATIONS === */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes backgroundMove {
  0% { background-position: 0 0; }
  100% { background-position: 60px 60px; }
}

/* === RESPONSIVE === */
@media (max-width: 768px) {
  .hero-stats {
    gap: 20px;
  }

  .stat-item {
    flex: 1;
    min-width: 80px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .btn {
    min-width: 250px;
  }

  .features-section {
    padding: 60px 0;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .feature-card {
    padding: 30px 20px;
  }

  .cta-section {
    padding: 60px 0;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .stat-number {
    font-size: 2rem;
  }

  .btn {
    min-width: 200px;
    padding: 14px 28px;
  }
}

/* === GRADIENT TEXT === */
.gradient-text {
  background: linear-gradient(45deg, #1a56db, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>