<template>
  <div
    class="game-card"
    :class="{ 'has-dropdown': mostrarDropdown }"
    :style="{ '--card-index': index }"
    @click="manejarClicEnCard"
  >
    <div class="card-image">
      <GameImage :src="game.imge_url" :alt="game.name" class="game-image" />
      <div class="image-overlay"></div>

      <div class="rating-badge" :class="game.metacritic ? claseMetacritic(game.metacritic) : 'mc-na'">
        {{ game.metacritic ?? '—' }}
      </div>

      <div class="card-actions-cluster">
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

        <button
          v-if="canChangeStatus"
          class="card-action-btn card-action-btn--status"
          :class="{ 'has-status': status }"
          :style="status ? { color: metaDelEstado?.color } : {}"
          @click.stop="mostrarDropdown = !mostrarDropdown"
          title="Change game status"
        >
          <i :class="'pi ' + (status ? metaDelEstado?.icon : 'pi-bookmark')"></i>
        </button>
      </div>

      <!-- Badge de estado (siempre visible si existe) -->
      <div
        v-if="status && canChangeStatus"
        class="status-badge"
        :style="{ background: metaDelEstado?.solidBg, color: metaDelEstado?.solidText }"
      >
        <i :class="'pi ' + metaDelEstado?.icon"></i>
        <span>{{ metaDelEstado?.label }}</span>
      </div>
    </div>

    <div class="card-content">
      <h3 class="game-title">{{ game.name }}</h3>

      <div class="game-info">
        <div class="info-item">
          <i class="pi pi-calendar"></i>
          <span>{{ game.release_date }}</span>
        </div>
      </div>

      <div class="card-footer">
        <span class="view-detail">View details</span>
        <i class="pi pi-arrow-right"></i>
      </div>
    </div>

    <!-- Dropdown de estado (fuera de card-image para no ser clipeado) -->
    <div v-if="mostrarDropdown && canChangeStatus" class="card-status-dropdown-wrap">
      <GameStatusDropdown
        :game-id="game.id"
        :current-status="status"
        @close="mostrarDropdown = false"
        @update:status="reenviarActualizacionEstado"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import GameImage from '../Image/GameImage.vue';
import GameStatusDropdown from './GameStatusDropdown.vue';
import { STATUS_META } from '../../utils/statusMeta.js';

// Card reutilizable que pinta un juego. La uso en el catalogo, en proximos
// lanzamientos, en favoritos del perfil, en saga del detalle, etc.
//
// Emite tres eventos al padre:
//   - "action": click en el boton de favorito (o de eliminar si removable).
//   - "click":  click en cualquier parte de la card (para navegar al detalle).
//   - "update:status": cuando se cambia el estado desde el dropdown interno.

const emit = defineEmits(['action', 'click', 'update:status']);

const props = defineProps({
  game: { type: Object, required: true },
  isFavorite: { type: Boolean, default: false },
  removable: { type: Boolean, default: false },
  isLoading: { type: Boolean, default: false },
  index: { type: Number, default: 0 },
  status: { type: String, default: null },
  // Permite ocultar el boton/dropdown de estado y el badge en escenarios
  // donde no tiene sentido (por ejemplo, juegos que aun no han salido:
  // no se puede marcar como "jugando" o "completado" un juego que no
  // existe todavia).
  canChangeStatus: { type: Boolean, default: true }
});

const mostrarDropdown = ref(false);

const metaDelEstado = computed(function () {
  if (props.status) {
    return STATUS_META[props.status];
  }
  return null;
});

function claseMetacritic(score) {
  if (score >= 80) {
    return 'mc-green';
  }
  if (score >= 50) {
    return 'mc-yellow';
  }
  return 'mc-red';
}

// Si el dropdown estaba abierto cerramos sin navegar; si no, emitimos
// "click" para que el componente padre navegue al detalle del juego.
function manejarClicEnCard() {
  if (mostrarDropdown.value) {
    mostrarDropdown.value = false;
    return;
  }
  emit('click');
}

function reenviarActualizacionEstado(payload) {
  emit('update:status', payload);
}
</script>

<style scoped src="./GameCard.css"></style>
