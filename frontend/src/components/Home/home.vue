<template>
  <div class="home-page">
    <!-- Hero Section - No Autenticado -->
    <section v-if="!estadoAutenticacion.usuario" class="hero-section">
      <video v-if="heroVideo" class="hero-video" autoplay muted loop playsinline>
        <source :src="heroVideo.video_url" type="video/mp4" />
      </video>
      <div class="hero-overlay-dark"></div>
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">Descubre, valora y comparte tus juegos favoritos</h1>
          <p class="hero-description">
            Explora miles de juegos, accede a críticas de la comunidad, crea tus tier lists personalizadas
            y conecta con otros jugadores apasionados.
          </p>

          <div class="hero-features">
            <div class="feature-item">
              <i class="pi pi-star-fill"></i>
              <span>Millones de reseñas</span>
            </div>
            <div class="feature-item">
              <i class="pi pi-users"></i>
              <span>Comunidad activa</span>
            </div>
            <div class="feature-item">
              <i class="pi pi-list"></i>
              <span>Tier lists personalizadas</span>
            </div>
          </div>

          <div class="hero-cta">
            <button class="btn btn-primary" @click="goToRegister">
              <i class="pi pi-user-plus"></i>
              Comenzar gratis
            </button>
            <button class="btn btn-secondary" @click="goToLogin">
              <i class="pi pi-sign-in"></i>
              Iniciar sesión
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Hero Section - Autenticado -->
    <section v-else class="hero-section">
      <video v-if="heroVideo" class="hero-video" autoplay muted loop playsinline>
        <source :src="heroVideo.video_url" type="video/mp4" />
      </video>
      <div class="hero-overlay-dark"></div>
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">¿Qué quieres explorar hoy?</h1>
          <p class="hero-description">
            Continúa descubriendo nuevos juegos, actualiza tus valoraciones y mantén tu colección de favoritos al día.
          </p>

          <div class="hero-quick-actions">
            <router-link to="/content/overview" class="quick-action-btn">
              <i class="pi pi-search"></i>
              <span>Explorar catálogo</span>
            </router-link>
            <router-link to="/user/profile" class="quick-action-btn">
              <i class="pi pi-heart"></i>
              <span>Mis favoritos</span>
            </router-link>
            <button class="quick-action-btn" @click="scrollToReleases">
              <i class="pi pi-calendar"></i>
              <span>Próximos lanzamientos</span>
            </button>
          </div>

          <div class="hero-cta">
            <button class="btn btn-primary" @click="goToExplore">
              <i class="pi pi-arrow-right"></i>
              Comenzar a explorar
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Top Games Section -->
    <section v-if="estadoAutenticacion.usuario !== null"  class="games-section">
      <div class="section-header">
        <h2>Los 3 mejores juegos</h2>
        <p>Clasificados por calificación de usuarios</p>
      </div>

      <Loader v-if="isLoading" message="Cargando juegos destacados..." />

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
            <span class="detail-category">
              <i class="pi pi-gamepad"></i>
              Videojuego
            </span>
            <h3>{{ topGames[0].name }}</h3>
            <p class="game-year">
              <i class="pi pi-calendar"></i>
              {{ topGames[0].release_date.split('-')[0] }}
            </p>
            <p class="game-description">Posicionado como el juego más calificado en nuestra base de datos. Esta
              selección refleja la preferencia de la comunidad gaming global.</p>
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

      <div v-else class="estado-vacio">
        <i class="pi pi-inbox"></i>
        <p>No hay juegos disponibles.</p>
    </div>
    </section>

    <!-- Proximos lanzamientos -->
    <section v-if="estadoAutenticacion.usuario !== null" id="proximos-section" class="proximos-section">
    <div class="section-header">
        <span class="section-eyebrow">
            <i class="pi pi-clock"></i>
            Próximamente
        </span>
        <h2>Próximos lanzamientos</h2>
        <p>Juegos que llegarán pronto</p>
    </div>

    <Loader v-if="isFutureLoading" message="Cargando próximos lanzamientos..." />

    <div v-else-if="futureReleases.length > 0" class="proximos-grid">
        <GameCard
            v-for="(game, index) in futureReleases"
            :key="game.id"
            :game="game"
            :index="index"
            :is-favorite="favorites.has(game.id)"
            :status="statuses.get(game.id) || null"
            @click="goToDetail(game.id)"
            @action="toggleFavorite"
            @update:status="handleStatusUpdate"
        />
    </div>

    <div v-else class="estado-vacio">
        <i class="pi pi-inbox"></i>
        <p>No hay próximos lanzamientos disponibles.</p>
    </div>
</section>

    <!-- Crea una cuenta nueva-->
    <section v-if="estadoAutenticacion.usuario === null" class="cta-section">
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
import { estadoAutenticacion } from "../../store/autenticacion.js";
import GameCard from "../Cards/GameCard.vue";
import Loader from "../Loader/Loader.vue";

export default {
  name: 'GameDetail',
  components: { GameCard, Loader },
  mixins: [jsHome]
};
</script>

<style scoped src="./style_home.css"></style>