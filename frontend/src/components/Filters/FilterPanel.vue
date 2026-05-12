<template>
  <Transition name="filter-slide">
    <div v-if="open" class="filter-panel">

      <div class="filter-section">
        <p class="filter-section-title">Ordenar por</p>
        <div class="filter-chips">
          <button
            v-for="opt in orderingOptions"
            :key="opt.value"
            class="filter-chip"
            :class="{ 'is-active': localOrdering === opt.value }"
            @click="toggleOrdering(opt.value)"
          >
            <i class="pi" :class="opt.icon"></i>
            {{ opt.label }}
          </button>
        </div>
      </div>

      <div class="filter-section">
        <p class="filter-section-title">Géneros</p>
        <div class="filter-chips">
          <button
            v-for="genre in genreOptions"
            :key="genre.value"
            class="filter-chip"
            :class="{ 'is-active': localGenres.includes(genre.value) }"
            @click="toggleGenre(genre.value)"
          >
            {{ genre.label }}
          </button>
        </div>
      </div>

      <div class="filter-section">
        <p class="filter-section-title">Plataformas</p>
        <div class="filter-chips">
          <button
            v-for="plat in platformOptions"
            :key="plat.value"
            class="filter-chip"
            :class="{ 'is-active': localPlatforms.includes(plat.value) }"
            @click="togglePlatform(plat.value)"
          >
            <i v-if="plat.icon" class="pi" :class="plat.icon"></i>
            {{ plat.label }}
          </button>
        </div>
      </div>

      <div class="filter-section">
        <p class="filter-section-title">Año de lanzamiento</p>
        <div class="filter-year-range">
          <div class="filter-year-input">
            <label>Desde</label>
            <input
              type="number"
              v-model.number="localDateFrom"
              min="1980"
              :max="currentYear"
              placeholder="1980"
            />
          </div>
          <div class="filter-year-sep">—</div>
          <div class="filter-year-input">
            <label>Hasta</label>
            <input
              type="number"
              v-model.number="localDateTo"
              min="1980"
              :max="currentYear"
              :placeholder="String(currentYear)"
            />
          </div>
        </div>
      </div>

      <div class="filter-actions">
        <button class="filter-btn-clear" @click="handleClear">
          <i class="pi pi-times"></i>
          Limpiar filtros
        </button>
        <button class="filter-btn-apply" @click="handleApply">
          <i class="pi pi-check"></i>
          Aplicar filtros
        </button>
      </div>

    </div>
  </Transition>
</template>

<script>
export default {
  name: 'FilterPanel',
  props: {
    open: {
      type: Boolean,
      default: false
    }
  },
  emits: ['apply', 'clear'],
  data() {
    return {
      localOrdering: '',
      localGenres: [],
      localPlatforms: [],
      localDateFrom: '',
      localDateTo: '',
      currentYear: new Date().getFullYear(),
      orderingOptions: [
        { value: '-rating', label: 'Mejor valorados', icon: 'pi-star-fill' },
        { value: '-released', label: 'Más recientes', icon: 'pi-calendar' },
        { value: 'released', label: 'Más antiguos', icon: 'pi-history' },
        { value: '-metacritic', label: 'Metacritic', icon: 'pi-chart-bar' },
        { value: 'name', label: 'A–Z', icon: 'pi-sort-alpha-down' },
        { value: '-added', label: 'Populares', icon: 'pi-bolt' }
      ],
      genreOptions: [
        { value: 'action', label: 'Acción' },
        { value: 'adventure', label: 'Aventura' },
        { value: 'role-playing-games-rpg', label: 'RPG' },
        { value: 'shooter', label: 'Shooter' },
        { value: 'strategy', label: 'Estrategia' },
        { value: 'simulation', label: 'Simulación' },
        { value: 'puzzle', label: 'Puzzle' },
        { value: 'sports', label: 'Deportes' },
        { value: 'racing', label: 'Carreras' },
        { value: 'indie', label: 'Indie' },
        { value: 'casual', label: 'Casual' },
        { value: 'arcade', label: 'Arcade' },
        { value: 'fighting', label: 'Lucha' },
        { value: 'platformer', label: 'Plataformas' }
      ],
      platformOptions: [
        { value: '4', label: 'PC', icon: 'pi-desktop' },
        { value: '187', label: 'PS5', icon: null },
        { value: '18', label: 'PS4', icon: null },
        { value: '186', label: 'Xbox X/S', icon: null },
        { value: '1', label: 'Xbox One', icon: null },
        { value: '7', label: 'Switch', icon: null },
        { value: '3', label: 'iOS', icon: 'pi-apple' },
        { value: '21', label: 'Android', icon: 'pi-android' }
      ]
    };
  },
  methods: {
    toggleOrdering(value) {
      this.localOrdering = this.localOrdering === value ? '' : value;
    },
    toggleGenre(value) {
      const idx = this.localGenres.indexOf(value);
      if (idx === -1) {
        this.localGenres.push(value);
      } else {
        this.localGenres.splice(idx, 1);
      }
    },
    togglePlatform(value) {
      const idx = this.localPlatforms.indexOf(value);
      if (idx === -1) {
        this.localPlatforms.push(value);
      } else {
        this.localPlatforms.splice(idx, 1);
      }
    },
    handleApply() {
      this.$emit('apply', {
        ordering: this.localOrdering,
        genres: [...this.localGenres],
        platforms: [...this.localPlatforms],
        dateFrom: this.localDateFrom || '',
        dateTo: this.localDateTo || ''
      });
    },
    handleClear() {
      this.localOrdering = '';
      this.localGenres = [];
      this.localPlatforms = [];
      this.localDateFrom = '';
      this.localDateTo = '';
      this.$emit('clear');
    }
  }
};
</script>

<style scoped src="./FilterPanel.css"></style>
