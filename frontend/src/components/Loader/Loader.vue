<template>
  <div class="loader" :class="[`loader-${size}`, { 'loader-fullheight': fullHeight }]">
    <div class="loader-spinner-wrap">
      <span class="loader-dot"></span>
      <span class="loader-dot"></span>
      <span class="loader-dot"></span>
    </div>
    <span v-if="message" class="loader-message">{{ message }}</span>
  </div>
</template>

<script>
export default {
  name: 'Loader',
  props: {
    message: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'medium',
      validator: (v) => ['small', 'medium', 'large'].includes(v)
    },
    fullHeight: {
      type: Boolean,
      default: false
    }
  }
};
</script>

<style scoped>
* {
  font-family: 'Sora', sans-serif;
}

.loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.1rem;
  width: 100%;
}

.loader-small {
  padding: 1.5rem 1rem;
}

.loader-medium {
  padding: 4rem 1rem;
}

.loader-large {
  padding: 6rem 1rem;
}

.loader-fullheight {
  min-height: 70vh;
  padding: 2rem 1rem;
}

.loader-spinner-wrap {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.loader-dot {
  display: inline-block;
  background: var(--color-primary);
  border-radius: 50%;
  animation: loader-bounce 1.4s infinite ease-in-out both;
}

.loader-small .loader-dot {
  width: 8px;
  height: 8px;
}

.loader-medium .loader-dot {
  width: 12px;
  height: 12px;
}

.loader-large .loader-dot {
  width: 16px;
  height: 16px;
}

.loader-dot:nth-child(1) {
  animation-delay: -0.32s;
}

.loader-dot:nth-child(2) {
  animation-delay: -0.16s;
}

.loader-dot:nth-child(3) {
  animation-delay: 0s;
}

@keyframes loader-bounce {
  0%, 80%, 100% {
    transform: scale(0.7);
    opacity: 0.6;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.loader-message {
  color: var(--color-text-medium);
  font-size: 0.92rem;
  font-weight: 500;
  text-align: center;
  letter-spacing: 0.01em;
}

.loader-small .loader-message {
  font-size: 0.82rem;
}

.loader-large .loader-message {
  font-size: 1.05rem;
}
</style>
