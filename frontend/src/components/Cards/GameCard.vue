<template>
  <div
    class="game-card"
    :class="{ 'has-dropdown': showDropdown }"
    :style="{ '--card-index': index }"
    @click="handleCardClick"
  >
    <!-- IMAGEN -->
    <div class="card-image">
      <GameImage :src="game.imge_url" :alt="game.name" class="game-image" />
      <div class="image-overlay"></div>

      <!-- Metacritic Badge -->
      <div class="rating-badge" :class="game.metacritic ? metacriticClass(game.metacritic) : 'mc-na'">
        {{ game.metacritic ?? '—' }}
      </div>

      <!-- Cluster de acciones (hover) -->
      <div class="card-actions-cluster">
        <!-- Favorito -->
        <button
          v-if="!removable"
          class="card-action-btn"
          :class="{ 'is-fav': isFavorite }"
          @click.stop="$emit('action', game.id)"
          :title="isFavorite ? 'Remove from favorites' : 'Add to favorites'"
        >
          <i :class="isFavorite ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
        </button>

        <!-- Eliminar (modo removable) -->
        <button
          v-else
          class="card-action-btn card-action-btn--danger"
          @click.stop="$emit('action', game.id)"
          title="Remove from favorites"
        >
          <i :class="isLoading ? 'pi pi-spin pi-spinner' : 'pi pi-trash'"></i>
        </button>

        <!-- Botón de estado -->
        <button
          class="card-action-btn card-action-btn--status"
          :class="{ 'has-status': status }"
          :style="status ? { color: statusMeta?.color } : {}"
          @click.stop="showDropdown = !showDropdown"
          title="Change game status"
        >
          <i :class="'pi ' + (status ? statusMeta?.icon : 'pi-bookmark')"></i>
        </button>
      </div>

      <!-- Badge de estado (siempre visible si existe) -->
      <div
        v-if="status"
        class="status-badge"
        :style="{ background: statusMeta?.solidBg, color: statusMeta?.solidText }"
      >
        <i :class="'pi ' + statusMeta?.icon"></i>
        <span>{{ statusMeta?.label }}</span>
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
        <span class="view-detail">View details</span>
        <i class="pi pi-arrow-right"></i>
      </div>
    </div>

    <!-- Dropdown de estado (fuera de card-image para no ser clipeado) -->
    <div v-if="showDropdown" class="card-status-dropdown-wrap">
      <GameStatusDropdown
        :game-id="game.id"
        :current-status="status"
        @close="showDropdown = false"
        @update:status="onStatusUpdate"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import GameImage from '../Image/GameImage.vue';
import GameStatusDropdown from './GameStatusDropdown.vue';
import { STATUS_META } from '../../utils/statusMeta.js';

const emit = defineEmits(['action', 'click', 'update:status']);

const props = defineProps({
  game: { type: Object, required: true },
  isFavorite: { type: Boolean, default: false },
  removable: { type: Boolean, default: false },
  isLoading: { type: Boolean, default: false },
  index: { type: Number, default: 0 },
  status: { type: String, default: null }
});

const showDropdown = ref(false);

const statusMeta = computed(() => props.status ? STATUS_META[props.status] : null);

function metacriticClass(score) {
  if (score >= 80) return 'mc-green';
  if (score >= 50) return 'mc-yellow';
  return 'mc-red';
}

function handleCardClick() {
  if (showDropdown.value) {
    showDropdown.value = false;
    return;
  }
  emit('click');
}

function onStatusUpdate(payload) {
  emit('update:status', payload);
}
</script>

<style scoped src="./GameCard.css"></style>
