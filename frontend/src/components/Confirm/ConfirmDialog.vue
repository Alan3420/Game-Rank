<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="confirmacion.state.open" class="ext-modal-overlay cw-scope" @click.self="confirmacion.responder(false)"
        @keydown.esc="confirmacion.responder(false)">
        <div class="ext-modal" role="alertdialog" aria-modal="true" aria-labelledby="confirm-dialog-title"
          aria-describedby="confirm-dialog-body">
          <div class="ext-modal__icon" :class="{ 'ext-modal__icon--danger': confirmacion.state.danger }">
            <i class="pi" :class="confirmacion.state.danger ? 'pi-trash' : 'pi-question'" aria-hidden="true"></i>
          </div>
          <h2 id="confirm-dialog-title" class="ext-modal__title">{{ confirmacion.state.title }}</h2>
          <p id="confirm-dialog-body" class="ext-modal__body">{{ confirmacion.state.message }}</p>
          <div class="ext-modal__actions">
            <button ref="cancelarRef" type="button" class="ext-modal__btn ext-modal__btn--cancel"
              @click="confirmacion.responder(false)">
              Cancel
            </button>
            <button type="button" class="ext-modal__btn"
              :class="confirmacion.state.danger ? 'ext-modal__btn--danger' : 'ext-modal__btn--confirm'"
              @click="confirmacion.responder(true)">
              {{ confirmacion.state.confirmLabel }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import { confirmacion } from '../../store/confirmacion';

// El foco arranca en "Cancel": en una accion destructiva la opcion segura
// es la que se activa si el usuario pulsa Enter sin pensar.
const cancelarRef = ref(null);
var focoAnterior = null;

watch(function () { return confirmacion.state.open; }, async function (abierto) {
  if (abierto) {
    focoAnterior = document.activeElement;
    await nextTick();
    cancelarRef.value?.focus();
  } else if (focoAnterior && focoAnterior.focus) {
    focoAnterior.focus();
    focoAnterior = null;
  }
});
</script>
