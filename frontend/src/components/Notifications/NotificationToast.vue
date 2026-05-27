<template>
  <Teleport to="body">
    <div class="toast-stack" aria-live="polite" aria-atomic="true">
      <TransitionGroup name="toast">
        <div v-for="item in notificaciones.state.items" :key="item.id" class="toast" :class="`toast-${item.type}`"
          role="status">
          <div class="toast-icon">
            <i class="pi" :class="item.icon"></i>
          </div>
          <div class="toast-body">
            <p class="toast-title">{{ item.title }}</p>
            <p class="toast-message">{{ item.message }}</p>
          </div>
          <button class="toast-close" @click="notificaciones.remove(item.id)" aria-label="Close notification">
            <i class="pi pi-times"></i>
          </button>
          <span class="toast-progress"></span>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { notificaciones } from '../../store/notificaciones';
</script>

<style scoped src="./styles_NotificationToast.css"></style>
