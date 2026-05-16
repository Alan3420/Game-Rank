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
            Explora miles de juegos, descubre valoraciones y opiniones de la comunidad, puntúa tus títulos favoritos y conecta con otros jugadores apasionados.
          </p>

          <div class="hero-features">
            <div class="feature-item">
              <i class="pi pi-star-fill"></i>
              <span>Reseñas de la comunidad</span>
            </div>
            <div class="feature-item">
              <i class="pi pi-users"></i>
              <span>Jugadores que comparten opiniones</span>
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
    <section v-if="estadoAutenticacion.usuario !== null" class="top-section">
      <div class="section-header">
        <span class="section-eyebrow">
          <i class="pi pi-trophy"></i>
          Ranking
        </span>
        <h2>Los mejores valorados</h2>
        <p>Clasificados por puntuación Metacritic</p>
      </div>

      <Loader v-if="isLoading" message="Cargando juegos destacados..." />

      <div v-else-if="topGames.length > 0" class="top-ranking">

        <!-- Rank 1 - Carta principal -->
        <article class="rank-card rank-card--first" @click="goToDetail(topGames[0].id)">
          <img class="rank-card-bg" :src="topGames[0].imge_url" :alt="topGames[0].name" />
          <div class="rank-card-overlay"></div>
          <span class="rank-num">1</span>
          <div class="rank-card-content">
            <span class="rank-best-badge"><i class="pi pi-crown"></i> Mejor valorado</span>
            <h3 class="rank-title">{{ topGames[0].name }}</h3>
            <span class="rank-year">{{ topGames[0].release_date?.split('-')[0] }}</span>
            <div class="rank-meta-wrap">
              <div class="rank-score" :class="metacriticColorClass(topGames[0].metacritic)">
                {{ topGames[0].metacritic ?? '—' }}
              </div>
              <span class="rank-score-label">Metacritic</span>
            </div>
          </div>
        </article>

        <!-- Ranks 2 y 3 -->
        <div class="rank-sub-grid">
          <article v-if="topGames[1]" class="rank-card rank-card--sub" @click="goToDetail(topGames[1].id)">
            <img class="rank-card-bg" :src="topGames[1].imge_url" :alt="topGames[1].name" />
            <div class="rank-card-overlay"></div>
            <span class="rank-num rank-num--sub">2</span>
            <div class="rank-card-content">
              <h3 class="rank-title">{{ topGames[1].name }}</h3>
              <span class="rank-year">{{ topGames[1].release_date?.split('-')[0] }}</span>
              <div class="rank-meta-wrap">
                <div class="rank-score rank-score--sm" :class="metacriticColorClass(topGames[1].metacritic)">
                  {{ topGames[1].metacritic ?? '—' }}
                </div>
                <span class="rank-score-label">Metacritic</span>
              </div>
            </div>
          </article>

          <article v-if="topGames[2]" class="rank-card rank-card--sub" @click="goToDetail(topGames[2].id)">
            <img class="rank-card-bg" :src="topGames[2].imge_url" :alt="topGames[2].name" />
            <div class="rank-card-overlay"></div>
            <span class="rank-num rank-num--sub">3</span>
            <div class="rank-card-content">
              <h3 class="rank-title">{{ topGames[2].name }}</h3>
              <span class="rank-year">{{ topGames[2].release_date?.split('-')[0] }}</span>
              <div class="rank-meta-wrap">
                <div class="rank-score rank-score--sm" :class="metacriticColorClass(topGames[2].metacritic)">
                  {{ topGames[2].metacritic ?? '—' }}
                </div>
                <span class="rank-score-label">Metacritic</span>
              </div>
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