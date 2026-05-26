<template>
    <div class="gsd-panel" ref="panelRef" @click.stop>
        <div class="gsd-options">
            <button
                v-for="key in STATUS_LIST"
                :key="key"
                class="gsd-option"
                :class="{ 'is-active': currentStatus === key, 'is-loading': loading }"
                @click.stop="manejarSeleccionEstado(key)"
                :disabled="loading"
            >
                <span>{{ STATUS_META[key].label }}</span>
                <i v-if="currentStatus === key" class="pi pi-check gsd-check"></i>
            </button>
        </div>

        <div v-if="currentStatus" class="gsd-divider"></div>

        <button
            v-if="currentStatus"
            class="gsd-remove"
            @click.stop="manejarEliminacionEstado"
            :disabled="loading"
        >
            <i v-if="loading" class="pi pi-spin pi-spinner"></i>
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

// Si el usuario hace click fuera del panel, lo cerramos.
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
        notificaciones.error("We couldn't save the status.", { title: 'Error' });

    } finally {
        loading.value = false;
    }
}

// Click en "Remove status": pide al backend borrar el estado y emite
// update:status con null para que el padre actualice su mapa.
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
        notificaciones.error("We couldn't remove the status.", { title: 'Error' });

    } finally {
        loading.value = false;
    }
}
</script>

<style scoped>
.gsd-panel {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.14);
    overflow: hidden;
    min-width: 160px;
}

.gsd-options {
    display: flex;
    flex-direction: column;
}

.gsd-option {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 9px 14px;
    border: none;
    background: transparent;
    color: var(--color-text);
    font-size: 0.84rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s;
    text-align: left;
    font-family: 'Sora', sans-serif;
}

.gsd-option:hover:not(:disabled) {
    background: var(--color-surface-hover);
}

.gsd-option.is-active {
    color: var(--color-primary);
    font-weight: 700;
    background: var(--color-primary-light);
}

.gsd-option:disabled {
    opacity: 0.55;
    cursor: not-allowed;
}

.gsd-check {
    font-size: 0.72rem;
    color: var(--color-primary);
    flex-shrink: 0;
}

.gsd-divider {
    height: 1px;
    background: var(--color-border-light);
    margin: 2px 0;
}

.gsd-remove {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    width: 100%;
    padding: 9px 14px;
    border: none;
    background: transparent;
    color: var(--color-danger);
    font-size: 0.84rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
    font-family: 'Sora', sans-serif;
}

.gsd-remove:hover:not(:disabled) {
    background: var(--color-danger-light);
}

.gsd-remove:disabled {
    opacity: 0.55;
    cursor: not-allowed;
}

[data-theme="dark"] .gsd-panel {
    border-color: var(--color-border);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}
</style>
