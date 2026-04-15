<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-text">
          <span class="hero-label">Bienvenido a Game Rank</span>
          <h1 class="hero-title">Descubre los mejores juegos</h1>
          <p class="hero-description">
            Tu plataforma minimalista para explorar, comparar y descubrir videojuegos. Encuentra títulos destacados ordenados por rating y crea tu lista personal de favoritos.
          </p>
          <div class="hero-cta">
            <button class="btn btn-primary" @click="goToLogin">
              <i class="pi pi-play"></i>
              Explorar ahora
            </button>
            <button class="btn btn-secondary" @click="goToRegister">
              <i class="pi pi-user-plus"></i>
              Crear cuenta
            </button>
          </div>
        </div>

        <div class="hero-visual">
          <div class="hero-accent"></div>
        </div>
      </div>
    </section>

    <!-- Top Games Section -->
    <section class="games-section">
      <div class="section-header">
        <h2>Los 3 mejores juegos</h2>
        <p>Clasificados por calificación de usuarios</p>
      </div>

      <div v-if="isLoading" class="loading-container">
        <span>Cargando juegos destacados...</span>
      </div>

      <div v-else-if="topGames.length > 0" class="games-layout">
        <!-- Juego principal (más grande) -->
        <article class="game-card game-card-featured">
          <div class="game-image-container featured-image">
            <img :src="topGames[0].imge_url" :alt="topGames[0].name" />
            <div class="game-rank">
              <span class="rank-label">1</span>
            </div>
            <div class="game-overlay">
              <div class="rating-display">
                <i class="pi pi-star-fill"></i>
                <span>{{ topGames[0].rating }}</span>
              </div>
            </div>
          </div>
          <div class="game-content featured-content">
            <h3>{{ topGames[0].name }}</h3>
            <p class="game-year">
              <i class="pi pi-calendar"></i>
              {{ topGames[0].release_date.split('-')[0] }}
            </p>
            <p class="game-description">Posicionado como el juego más calificado en nuestra base de datos. Esta selección refleja la preferencia de la comunidad gaming global.</p>
          </div>
        </article>

        <!-- Juegos secundarios (más pequeños) -->
        <div class="games-secondary">
          <article v-for="(game, idx) in topGames.slice(1, 3)" :key="game.id" class="game-card game-card-secondary">
            <div class="game-image-container">
              <img :src="game.imge_url" :alt="game.name" />
              <div class="game-rank">
                <span class="rank-label">{{ idx + 2 }}</span>
              </div>
              <div class="game-overlay secondary-overlay">
                <div class="rating-badge">{{ game.rating }}</div>
              </div>
            </div>
            <div class="game-content">
              <h4>{{ game.name }}</h4>
              <p class="game-meta">
                <i class="pi pi-calendar"></i>
                {{ game.release_date.split('-')[0] }}
              </p>
            </div>
          </article>
        </div>
      </div>

      <div v-else class="empty-state">
        <i class="pi pi-inbox"></i>
        <p>No hay juegos disponibles en este momento</p>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-content">
        <h2>Únete a la comunidad</h2>
        <p>Explora miles de juegos, comparte tu opinión y descubre títulos que se adapten a tus preferencias.</p>
        <button class="btn btn-accent" @click="goToRegister">
          <i class="pi pi-check"></i>
          Comenzar ahora
        </button>
      </div>
    </section>
  </div>
</template>

<script>
import { getContentOverview } from '../services/resume_cards.js';

export default {
  data() {
    return {
      topGames: [],
      isLoading: true
    };
  },
  async mounted() {
    await this.loadTopGames();
  },
  methods: {
    async loadTopGames() {
      this.isLoading = true;
      try {
        const response = await getContentOverview(1);
        console.log('API Response:', response);
        
        let games = [];
        if (response && response.games && Array.isArray(response.games)) {
          games = response.games;
        } else if (Array.isArray(response)) {
          games = response;
        }
        
        const validGames = games.filter(game => game.rating && game.rating > 0);
        console.log('Valid games found:', validGames.length);
        
        const sorted = validGames.sort((a, b) => b.rating - a.rating);
        this.topGames = sorted.slice(0, 3);
        console.log('Top 3 games:', this.topGames);
      } catch (error) {
        console.error('Error loading top games:', error);
      } finally {
        this.isLoading = false;
      }
    },
    goToLogin() {
      const token = localStorage.getItem("token")
      if (token) {
        this.$router.push('/content/overview');
      } else {
        this.$router.push('/login');
      }
    },
    goToRegister(){
      this.$router.push("/register");
    }
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fb 0%, #f3f4fa 100%);
  color: #1f1f35;
}

/* Hero Section */
.hero-section {
  padding: 80px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.hero-content {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 60px;
  align-items: center;
}

.hero-text {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.hero-label {
  display: inline-block;
  width: fit-content;
  padding: 8px 16px;
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.hero-title {
  margin: 0;
  font-size: 3.5rem;
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: #1f1f35;
}

.hero-description {
  margin: 0;
  font-size: 1.1rem;
  line-height: 1.8;
  color: #555;
  max-width: 500px;
}

.hero-cta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 12px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 28px;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.btn-primary {
  background: #6366f1;
  color: white;
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(99, 102, 241, 0.4);
}

.btn-secondary {
  background: rgba(99, 102, 241, 0.08);
  color: #6366f1;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.btn-secondary:hover {
  background: rgba(99, 102, 241, 0.15);
  transform: translateY(-2px);
}

.btn-accent {
  background: white;
  color: #6366f1;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.btn-accent:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
}

.hero-visual {
  position: relative;
  height: 400px;
}

.hero-accent {
  position: absolute;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
}

/* Games Section */
.games-section {
  padding: 80px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.section-header {
  margin-bottom: 48px;
  text-align: center;
}

.section-header h2 {
  margin: 0 0 8px;
  font-size: 2.5rem;
  font-weight: 900;
  color: #1f1f35;
}

.section-header p {
  margin: 0;
  font-size: 1.05rem;
  color: #888;
}

.games-layout {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 32px;
  grid-auto-rows: auto;
}

.game-card-featured {
  grid-row: 1 / 3;
}

.games-secondary {
  display: grid;
  gap: 24px;
}

.game-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.game-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.08);
}

.game-image-container {
  position: relative;
  overflow: hidden;
  background: #e5e7eb;
}

.game-card-featured .game-image-container {
  height: 500px;
}

.game-card-secondary .game-image-container {
  height: 240px;
}

.featured-image {
  height: 100%;
  min-height: 500px;
}

.game-image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.game-card:hover .game-image-container img {
  transform: scale(1.05);
}

.game-rank {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 2;
}

.rank-label {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: rgba(31, 31, 53, 0.9);
  border-radius: 50%;
  font-size: 1.5rem;
  font-weight: 900;
  color: #a5f3fc;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.15);
}

.game-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(31, 31, 53, 0.8) 0%, transparent 60%);
  display: flex;
  align-items: flex-end;
  justify-content: flex-start;
  padding: 24px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.game-card:hover .game-overlay {
  opacity: 1;
}

.secondary-overlay {
  align-items: flex-start;
  justify-content: flex-end;
  padding: 16px;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 12px 16px;
  border-radius: 12px;
  font-weight: 800;
  color: #1f1f35;
}

.rating-display i {
  color: #fbbf24;
  font-size: 1.1rem;
}

.rating-badge {
  display: inline-flex;
  align-items: center;
  background: white;
  padding: 8px 12px;
  border-radius: 10px;
  font-weight: 700;
  color: #1f1f35;
  font-size: 0.95rem;
}

.game-content {
  padding: 32px 24px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.featured-content {
  padding: 32px 24px;
}

.game-content h3 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 800;
  color: #1f1f35;
  line-height: 1.2;
}

.game-card-secondary .game-content h4 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f1f35;
}

.game-year,
.game-meta {
  margin: 0;
  font-size: 0.95rem;
  color: #888;
  display: flex;
  align-items: center;
  gap: 6px;
}

.game-year i,
.game-meta i {
  font-size: 0.85rem;
}

.game-description {
  margin: 8px 0 0;
  font-size: 1rem;
  color: #555;
  line-height: 1.6;
}

.loading-container {
  grid-column: 1 / -1;
  padding: 60px 20px;
  text-align: center;
  color: #6366f1;
  font-size: 1.05rem;
}

.empty-state {
  grid-column: 1 / -1;
  padding: 80px 20px;
  text-align: center;
  color: #888;
}

.empty-state i {
  display: block;
  font-size: 3.5rem;
  color: #ccc;
  margin-bottom: 16px;
}

/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  padding: 80px 40px;
  text-align: center;
  color: white;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.cta-content h2 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 900;
}

.cta-content p {
  margin: 0;
  font-size: 1.1rem;
  opacity: 0.95;
  line-height: 1.8;
}

/* Responsive */
@media (max-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .hero-visual {
    display: none;
  }

  .games-layout {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .game-card-featured {
    grid-row: auto;
  }
}

@media (max-width: 768px) {
  .hero-section,
  .games-section,
  .cta-section {
    padding: 60px 24px;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .section-header h2 {
    font-size: 2rem;
  }

  .games-layout {
    grid-template-columns: 1fr;
  }

  .game-card-featured .game-image-container {
    height: 300px;
  }

  .game-content {
    padding: 24px 16px;
  }

  .cta-content h2 {
    font-size: 2rem;
  }
}

@media (max-width: 640px) {
  .hero-section,
  .games-section,
  .cta-section {
    padding: 40px 16px;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-description {
    font-size: 1rem;
  }

  .hero-cta {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    padding: 12px 20px;
  }

  .section-header h2 {
    font-size: 1.75rem;
  }

  .section-header p {
    font-size: 0.95rem;
  }

  .game-card-featured .game-image-container {
    height: 220px;
  }

  .game-card-secondary .game-image-container {
    height: 180px;
  }

  .game-content h3 {
    font-size: 1.4rem;
  }

  .game-card-secondary .game-content h4 {
    font-size: 1.1rem;
  }

  .rank-label {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }

  .cta-content h2 {
    font-size: 1.75rem;
  }
  .cta-content p {
    font-size: 1rem;
  }
}
</style>
