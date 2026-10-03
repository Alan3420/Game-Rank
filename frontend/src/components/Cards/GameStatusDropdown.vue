<template>
    <div class="gsd-panel cw-scope" ref="panelRef" @click.stop role="menu" aria-label="Collection status">
        <div class="gsd-options">
            <button
                v-for="key in STATUS_LIST"
                :key="key"
                type="button"
                role="menuitemradio"
                :aria-checked="currentStatus === key"
                class="gsd-option cw-frame"
                :class="['cw-frame--' + key, { 'is-active': currentStatus === key, 'is-loading': loading }]"
                @click.stop="manejarSeleccionEstado(key)"
                :disabled="loading"
            >
                <i aria-hidden="true" :class="'pi ' + STATUS_META[key].icon + ' gsd-icon'"></i>
                <span class="gsd-label">{{ STATUS_META[key].label }}</span>
                <i aria-hidden="true" v-if="currentStatus === key" class="pi pi-check gsd-check"></i>
            </button>
        </div>

        <div v-if="currentStatus" class="gsd-divider"></div>

        <button
            v-if="currentStatus"
            type="button"
            role="menuitem"
            class="gsd-remove"
            @click.stop="manejarEliminacionEstado"
            :disabled="loading"
        >
            <i aria-hidden="true" v-if="loading" class="pi pi-spin pi-spinner"></i>
            <span v-else>Remove status</span>
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { STATUS_META, STATUS_LIST } from '../../utils/statusMeta.js';
import { establecerEstadoDeJuego, eliminarEstadoDeJuego } from '../../services/user_game_status.js';
import { notificaciones } from '../../store/notificaciones.js';

// Dropdown que se muestra encima de una card para asignar (o quitar) el
// estado en que el usuario tiene un juego. Emite "update:status" cuando
// el backend confirma el cambio, y "close" cuando hay que ocultarse.

const props = defineProps({
    gameId: { type: Number, required: true },
    currentStatus: { type: String, default: null }
});

const emit = defineEmits(['close', 'update:status']);

const panelRef = ref(null);
const loading = ref(false);

function alClicEnDocumento(e) {
    if (panelRef.value && !panelRef.value.contains(e.target)) {
        emit('close');
    }
}

// Registramos el listener en setTimeout(0) para que el mismo click que
// abrio el dropdown no lo cierre de inmediato (porque ese click se
// propaga al document despues del onClick que nos monto).
onMounted(function () {
    setTimeout(function () {
        document.addEventListener('mousedown', alClicEnDocumento);
    }, 0);
});

onBeforeUnmount(function () {
    document.removeEventListener('mousedown', alClicEnDocumento);
});

// Click en una de las opciones de estado. Si el usuario pulso el estado
// que ya estaba activo, no hacemos nada (solo cerramos el dropdown).
async function manejarSeleccionEstado(estado) {

    if (loading.value || estado === props.currentStatus) {
        emit('close');
        return;
    }

    loading.value = true;

    try {
        await establecerEstadoDeJuego(props.gameId, estado);
        emit('update:status', { gameId: props.gameId, status: estado });
        notificaciones.success('Status updated to "' + STATUS_META[estado].label + '".', { title: 'Status saved' });
        emit('close');

    } catch (error) {
        notificaciones.error("Status wasn't saved. Check your connection and try again.", { title: 'Error' });

    } finally {
        loading.value = false;
    }
}

async function manejarEliminacionEstado() {

    if (loading.value) {
        return;
    }

    loading.value = true;

    try {
        await eliminarEstadoDeJuego(props.gameId);
        emit('update:status', { gameId: props.gameId, status: null });
        notificaciones.success('Status removed.', { title: 'Status removed' });
        emit('close');

    } catch (error) {
        notificaciones.error("Status wasn't removed. Check your connection and try again.", { title: 'Error' });

    } finally {
        loading.value = false;
    }
}
</script>

<style scoped>
/* Menu de estado del mundo "carta coleccionable": cada opcion lleva el
   color de su estado; la activa se rellena con el, como el marco. */
.gsd-panel {
    min-width: 180px;
    padding: 4px;
    overflow: hidden;
    border: 1px solid var(--gd-rule);
    border-radius: 12px;
    background: var(--gd-face);
    box-shadow: var(--gd-raise);
}

.gsd-options {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.gsd-option {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: var(--gd-ink);
    font-size: 0.92rem;
    font-weight: 600;
    text-align: left;
    cursor: pointer;
    transition: background-color 150ms ease, color 150ms ease;
}

.gsd-icon {
    font-size: 0.85rem;
    color: var(--gd-frame);
}

.gsd-label {
    flex: 1;
}

.gsd-option.is-active {
    background: var(--gd-frame);
    color: var(--gd-on-frame-now);
}

.gsd-option.is-active .gsd-icon,
.gsd-check {
    color: inherit;
}

.gsd-check {
    flex-shrink: 0;
    font-size: 0.75rem;
}

.gsd-option:disabled,
.gsd-remove:disabled {
    opacity: 0.55;
    cursor: not-allowed;
}

.gsd-divider {
    height: 1px;
    margin: 4px 0;
    background: var(--gd-rule);
}

.gsd-remove {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    width: 100%;
    padding: 8px 10px;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: var(--gd-danger);
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 150ms ease;
}

@media (hover: hover) and (pointer: fine) {
    .gsd-option:not(.is-active):hover:not(:disabled),
    .gsd-remove:hover:not(:disabled) {
        background: var(--gd-ground);
    }
}
</style>
