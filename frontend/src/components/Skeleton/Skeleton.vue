<template>
  <span
    class="skeleton"
    :class="{ 'skeleton--circle': circle, 'skeleton--on-dark': onDark }"
    :style="estilo"
    aria-hidden="true"
  ></span>
</template>

<script setup>
import { computed } from 'vue';

// Bloque base del skeleton. Las vistas lo combinan para imitar el layout
// real mientras cargan los datos. Si no se pasa width/height, el tamano lo
// define la clase que le ponga el padre (las clases scoped del padre se
// aplican al elemento raiz de este componente).

const props = defineProps({
  width: { type: String, default: null },
  height: { type: String, default: null },
  radius: { type: String, default: null },
  circle: { type: Boolean, default: false },
  // Para skeletons sobre fondos oscuros (hero del detalle, etc.)
  onDark: { type: Boolean, default: false }
});

const estilo = computed(function () {
  const s = {};
  if (props.width) {
    s.width = props.width;
  }
  if (props.height) {
    s.height = props.height;
  }
  if (props.circle && props.width && !props.height) {
    s.height = props.width;
  }
  if (props.radius) {
    s.borderRadius = props.radius;
  }
  return s;
});
</script>

<style scoped>
.skeleton {
  display: block;
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  background: var(--color-skeleton-base);
  flex-shrink: 0;
  max-width: 100%;
}

.skeleton::after {
  content: '';
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--color-skeleton-highlight) 50%,
    transparent 100%
  );
  animation: skeleton-shimmer 1.4s ease-in-out infinite;
}

.skeleton--circle {
  border-radius: 50%;
}

.skeleton--on-dark {
  background: rgba(255, 255, 255, 0.12);
}

.skeleton--on-dark::after {
  background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.14) 50%, transparent 100%);
}

@keyframes skeleton-shimmer {
  100% {
    transform: translateX(100%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton::after {
    animation: none;
  }
}
</style>
