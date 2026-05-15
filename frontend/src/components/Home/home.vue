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
        <h2>Los mejores juegos</h2>
        <p>Clasificados por calificación de la comunidad</p>
      </div>

      <Loader v-if="isLoading" message="Cargando juegos destacados..." />

      <div v-else-if="topGames.length > 0" class="top-podium">

        <!-- Rank 2 -->
        <div class="top-slot top-slot--2">
          <article v-if="topGames[1]" class="top-card top-card--silver" @click="goToDetail(topGames[1].id)">
            <div class="top-card-img-wrap">
              <img :src="topGames[1].imge_url" :alt="topGames[1].name" />
              <div class="top-card-img-overlay"></div>
              <div class="top-card-medal medal--silver">
                <span class="medal-num">2</span>
                <i class="pi pi-trophy"></i>
              </div>
            </div>
            <div class="top-card-body">
              <h3 class="top-card-name">{{ topGames[1].name }}</h3>
              <span class="top-card-year">
                <i class="pi pi-calendar"></i>
                {{ topGames[1].release_date.split('-')[0] }}
              </span>
              <div class="top-card-rating">
                <i class="pi pi-star-fill"></i>
                <span class="top-card-score">{{ topGames[1].rating }}</span>
                <span class="top-card-denom">/ 10</span>
              </div>
            </div>
          </article>
        </div>

        <!-- Rank 1 (centro, destacado) -->
        <div class="top-slot top-slot--1">
          <div class="top-best-label">
            <i class="pi pi-crown"></i>
            Mejor valorado
          </div>
          <article class="top-card top-card--gold" @click="goToDetail(topGames[0].id)">
            <div class="top-card-img-wrap">
              <img :src="topGames[0].imge_url" :alt="topGames[0].name" />
              <div class="top-card-img-overlay"></div>
              <div class="top-card-medal medal--gold">
                <span class="medal-num">1</span>
                <i class="pi pi-trophy"></i>
              </div>
            </div>
            <div class="top-card-body">
              <h3 class="top-card-name">{{ topGames[0].name }}</h3>
              <span class="top-card-year">
                <i class="pi pi-calendar"></i>
                {{ topGames[0].release_date.split('-')[0] }}
              </span>
              <div class="top-card-rating">
                <i class="pi pi-star-fill"></i>
                <span class="top-card-score">{{ topGames[0].rating }}</span>
                <span class="top-card-denom">/ 10</span>
              </div>
            </div>
          </article>
        </div>

        <!-- Rank 3 -->
        <div class="top-slot top-slot--3">
          <article v-if="topGames[2]" class="top-card top-card--bronze" @click="goToDetail(topGames[2].id)">
            <div class="top-card-img-wrap">
              <img :src="topGames[2].imge_url" :alt="topGames[2].name" />
              <div class="top-card-img-overlay"></div>
              <div class="top-card-medal medal--bronze">
                <span class="medal-num">3</span>
                <i class="pi pi-trophy"></i>
              </div>
            </div>
            <div class="top-card-body">
              <h3 class="top-card-name">{{ topGames[2].name }}</h3>
              <span class="top-card-year">
                <i class="pi pi-calendar"></i>
                {{ topGames[2].release_date.split('-')[0] }}
              </span>
              <div class="top-card-rating">
                <i class="pi pi-star-fill"></i>
                <span class="top-card-score">{{ topGames[2].rating }}</span>
                <span class="top-card-denom">/ 10</span>
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