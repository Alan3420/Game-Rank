<template>
  <div ref="raiz" class="mini cw-frame" :class="[status ? `cw-frame--${status}` : '', { 'mini--menu': menuAbierto, 'mini--two-actions': showFavorite && canChangeStatus }]"
    @keydown.esc="menuAbierto = false">
    <component :is="game.id ? 'router-link' : 'div'" :to="game.id ? '/game/' + game.id : undefined" class="mini__link">
      <span class="mini__band">
        <span class="mini__name" :title="game.name">{{ game.name }}</span>
        <span class="cw-mc mini__mc" :class="claseMetacritic(game.metacritic)">
          <span class="sr-only">Metacritic</span>{{ game.metacritic ?? '—' }}
        </span>
      </span>
      <span class="mini__art">
        <GameImage :src="game.imge_url" alt="" width="640" height="480" />
      </span>
      <span class="mini__set">
        <span class="mini__set-line">
          <span v-if="game.id" class="mini__number">No. {{ game.id }}</span>
          <span v-if="game.release_date || game.id">{{ game.release_date ? game.release_date.split('-')[0] : 'TBA' }}</span>
        </span>
        <span class="mini__set-line mini__set-line--stamp">
          <span v-if="status" class="mini__stamp">
            <i aria-hidden="true" :class="'pi ' + STATUS_META[status].icon"></i>
            {{ STATUS_META[status].label }}
          </span>
        </span>
      </span>
    </component>
    <button
      v-if="canChangeStatus"
      type="button"
      class="mini__action mini__status-btn"
      aria-haspopup="menu"
      :aria-expanded="menuAbierto"
      :aria-label="'Change status of ' + game.name"
      @click="menuAbierto = !menuAbierto"
    >
      <i aria-hidden="true" class="pi pi-bookmark"></i>
    </button>
    <Transition name="gsd">
      <div v-if="menuAbierto" class="mini__menu">
        <GameStatusDropdown
          :game-id="game.id"
          :current-status="status"
          @close="menuAbierto = false"
          @update:status="$emit('update:status', $event)"
        />
      </div>
    </Transition>
    <button
      v-if="showFavorite"
      type="button"
      class="mini__action mini__fav"
      :aria-pressed="favorite"
      :aria-label="(favorite ? 'Remove ' : 'Add ') + game.name + (favorite ? ' from favorites' : ' to favorites')"
      @click="$emit('toggle-favorite', game.id)"
    >
      <i aria-hidden="true" :class="favorite ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
    </button>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue';
import GameImage from '../Image/GameImage.vue';
import GameStatusDropdown from '../Cards/GameStatusDropdown.vue';
import { STATUS_META } from '../../utils/statusMeta.js';
import { claseMetacritic } from '../../utils/metacritic.js';

// Carta pequena del mundo "carta coleccionable". La comparten la ficha
// (saga) y la Home (album, tendencias...). El marco toma el color del
// estado del jugador, igual que la carta grande de la ficha.

defineProps({
  game: { type: Object, required: true },
  status: { type: String, default: null },
  favorite: { type: Boolean, default: false },
  showFavorite: { type: Boolean, default: false },
  // Muestra el boton y el menu de estado (solo favoritos ya lanzados)
  canChangeStatus: { type: Boolean, default: false }
});

defineEmits(['toggle-favorite', 'update:status']);

const raiz = ref(null);
const menuAbierto = ref(false);

// El menu se cierra al pulsar fuera de la carta
function cerrarSiFuera(evento) {
  if (raiz.value && !raiz.value.contains(evento.target)) {
    menuAbierto.value = false;
  }
}

watch(menuAbierto, function (abierto) {
  if (abierto) {
    document.addEventListener('mousedown', cerrarSiFuera);
  } else {
    document.removeEventListener('mousedown', cerrarSiFuera);
  }
});

onBeforeUnmount(function () {
  document.removeEventListener('mousedown', cerrarSiFuera);
});

</script>

<style scoped>
.mini {
  position: relative;
  height: 100%;
  padding: 6px;
  border-radius: 16px;
  background: var(--gd-frame);
  box-shadow: var(--gd-raise);
  transition: transform 200ms var(--ease-out), background-color 320ms var(--ease-out);
}

.mini__link {
  display: flex;
  flex-direction: column;
  gap: 8px;
  height: 100%;
  padding: 10px;
  border-radius: 11px;
  background: var(--gd-face);
  color: var(--gd-ink);
  text-decoration: none;
}

.mini__band {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  height: 2.35rem;
}

.mini__name {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  overflow: hidden;
  font-family: 'Barlow Condensed', 'Barlow', sans-serif;
  font-size: 1.1rem;
  font-weight: 800;
  line-height: 1.05;
  overflow-wrap: anywhere;
}

.mini__art {
  display: block;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  border-radius: 7px;
  background: var(--gd-ground);
}

.mini__art :deep(img) {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* pie de set fijo de dos lineas: todas las cartas miden lo mismo tengan
   o no sello, y las acciones se alinean con la segunda linea */
.mini__set {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.8rem;
  color: var(--gd-ink-3);
  font-variant-numeric: tabular-nums;
}

.mini__set-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.mini__set-line--stamp {
  min-height: 24px;
  padding-right: 34px;
}

.mini--two-actions .mini__set-line--stamp {
  padding-right: 68px;
}

.mini__number {
  white-space: nowrap;
  font-family: 'Barlow Condensed', 'Barlow', sans-serif;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--gd-ink-2);
}

.mini__stamp {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--gd-frame);
  color: var(--gd-on-frame-now);
  font-size: 0.72rem;
  font-weight: 700;
}

.mini__stamp .pi {
  font-size: 0.65rem;
}

.mini--menu {
  z-index: 30;
}

.mini__status-btn {
  right: 44px;
}

.mini__menu {
  position: absolute;
  right: 6px;
  bottom: 46px;
  z-index: 40;
  transform-origin: bottom right;
}

.gsd-enter-active {
  transition: opacity 160ms var(--ease-out), transform 160ms var(--ease-out);
}

.gsd-leave-active {
  transition: opacity 100ms var(--ease-out);
}

.gsd-enter-from {
  opacity: 0;
  transform: scale(0.96);
}

.gsd-leave-to {
  opacity: 0;
}

.mini__action {
  position: absolute;
  right: 12px;
  bottom: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--gd-ink-3);
  cursor: pointer;
  transition: background-color 150ms ease, color 150ms ease, transform 160ms var(--ease-out);
}

.mini__fav[aria-pressed="true"],
.mini__status-btn[aria-expanded="true"] {
  color: var(--gd-ink);
}

.mini__status-btn {
  right: 44px;
  color: var(--gd-frame);
}

.mini:not([class*="cw-frame--"]) .mini__status-btn {
  color: var(--gd-ink-3);
}

.mini__action:active {
  transform: scale(0.92);
}

@media (hover: hover) and (pointer: fine) {
  .mini:hover {
    transform: translateY(-3px);
  }

  .mini__action:hover {
    background: var(--gd-ground);
    color: var(--gd-ink);
  }
}

/* carta estrecha: el nombre ocupa toda la banda y la nota de Metacritic
   pasa a la esquina de la portada */
@media (max-width: 480px) {
  .mini__link {
    position: relative;
  }

  .mini__band {
    display: block;
    height: 2.15rem;
  }

  .mini__name {
    font-size: 0.95rem;
  }

  .mini__mc {
    position: absolute;
    top: calc(10px + 2.15rem + 8px + 6px);
    right: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  }
}
</style>
