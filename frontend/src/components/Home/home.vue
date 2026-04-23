<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-text">
          <span class="hero-label">Bienvenido a Game Rank</span>
          <h1 class="hero-title">Descubre los mejores juegos</h1>
          <p class="hero-description">
            Tu mejor plataforma para explorar, comparar y descubrir videojuegos. Encuentra títulos destacados ordenados por rating y crea tu lista personal de favoritos.
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
  import jsHome from "./script_home.js";
  import "./style_home.css";

  export default {
    name: 'GameDetail',
    mixins: [jsHome]
  };
</script>