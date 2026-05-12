<template>
  <div class="game-card" :style="{ '--card-index': index }" @click="handleCardClick">
    <!-- IMAGEN -->
    <div class="card-image">
      <GameImage :src="game.imge_url" :alt="game.name" class="game-image" />
      <div class="image-overlay"></div>

      <!-- Botón Acciones (Favorito o Eliminar) -->
      <div class="card-action" :class="{ 'is-loading': isLoading }">
        <!-- Modo Favorito (corazón) -->
        <template v-if="!removable">
          <i
            v-if="isFavorite"
            @click.stop="$emit('action', game.id)"
            class="pi pi-heart-fill"
          ></i>
          <i v-else @click.stop="$emit('action', game.id)" class="pi pi-heart"></i>
        </template>

        <!-- Modo Eliminar (basura) -->
        <template v-else>
          <i
            @click.stop="$emit('action', game.id)"
            :class="isLoading ? 'pi pi-spin pi-spinner' : 'pi pi-trash'"
          ></i>
        </template>
      </div>

      <!-- Rating Badge -->
      <div class="rating-badge">
        <i class="pi pi-star-fill"></i>
        <span>{{ game.rating }}</span>
      </div>
    </div>

    <!-- CONTENIDO -->
    <div class="card-content">
      <h3 class="game-title">{{ game.name }}</h3>

      <div class="game-info">
        <div class="info-item">
          <i class="pi pi-calendar"></i>
          <span>{{ game.release_date }}</span>
        </div>
      </div>

      <!-- FOOTER -->
      <div class="card-footer">
        <span class="view-detail">Ver detalles</span>
        <i class="pi pi-arrow-right"></i>
      </div>
    </div>
  </div>
</template>

<script setup>
import GameImage from '../Image/GameImage.vue';

const emit = defineEmits(['action', 'click']);

defineProps({
  game: {
    type: Object,
    required: true
  },
  isFavorite: {
    type: Boolean,
    default: false
  },
  removable: {
    type: Boolean,
    default: false
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  index: {
    type: Number,
    default: 0
  }
});

const handleCardClick = () => {
  emit('click');
};
</script>

<style scoped src="./GameCard.css"></style>
