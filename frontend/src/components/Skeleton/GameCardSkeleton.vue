<template>
  <div class="game-card-skeleton" aria-hidden="true">
    <Skeleton class="gcs-image" radius="16px 16px 0 0" />
    <div class="gcs-content">
      <Skeleton width="80%" height="1.1rem" />
      <Skeleton width="45%" height="0.85rem" />
      <div class="gcs-footer">
        <Skeleton width="35%" height="0.8rem" />
        <Skeleton width="1rem" height="0.8rem" />
      </div>
    </div>
  </div>
</template>

<script setup>
import Skeleton from './Skeleton.vue';

// Placeholder con la misma estructura que GameCard (imagen + titulo +
// fecha + footer) para que la grilla no salte al llegar los datos.
</script>

<style scoped>
.game-card-skeleton {
  background: var(--color-surface);
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  border: 1px solid var(--color-border-lightest);
}

.gcs-image {
  width: 100%;
  height: 200px;
}

.gcs-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1.25rem;
}

.gcs-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.4rem;
  padding-top: 0.9rem;
  border-top: 1px solid var(--color-border-lightest);
}
</style>
