<template>
  <div class="table-skeleton" aria-hidden="true">
    <div class="ts-head">
      <Skeleton v-for="c in columns" :key="'h' + c" width="60%" height="0.75rem" />
    </div>
    <div v-for="r in rows" :key="r" class="ts-row">
      <div class="ts-user">
        <Skeleton circle width="40px" />
        <div class="ts-user-text">
          <Skeleton width="120px" height="0.85rem" />
          <Skeleton width="80px" height="0.7rem" />
        </div>
      </div>
      <Skeleton v-for="c in columns - 1" :key="c" :width="c === columns - 1 ? '60px' : '75%'" height="0.85rem" />
    </div>
  </div>
</template>

<script setup>
import Skeleton from './Skeleton.vue';

// Skeleton de las tablas del panel de admin. La primera columna imita la
// celda de usuario (avatar + nombre + nickname).

const props = defineProps({
  rows: { type: Number, default: 6 },
  columns: { type: Number, default: 5 }
});
</script>

<style scoped>
.table-skeleton {
  width: 100%;
}

.ts-head,
.ts-row {
  display: grid;
  grid-template-columns: 2fr repeat(v-bind('props.columns - 1'), 1fr);
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
}

.ts-head {
  background: var(--color-surface-alt);
}

.ts-row {
  border-bottom: 1px solid var(--color-border-lightest);
}

.ts-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ts-user-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>
