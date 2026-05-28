<template>
  <Transition name="filter-slide">
    <div v-if="open" class="filter-panel">

      <div class="filter-section">
        <p class="filter-section-title">Sort by</p>
        <div class="filter-chips">
          <button
            v-for="opt in opcionesDeOrden"
            :key="opt.value"
            class="filter-chip"
            :class="{ 'is-active': ordenLocal === opt.value }"
            @click="alternarOrden(opt.value)"
          >
            <i class="pi" :class="opt.icon"></i>
            {{ opt.label }}
          </button>
        </div>
      </div>

      <div class="filter-section">
        <p class="filter-section-title">Genres</p>
        <div class="filter-chips">
          <button
            v-for="genre in opcionesDeGenero"
            :key="genre.value"
            class="filter-chip"
            :class="{ 'is-active': generosLocales.includes(genre.value) }"
            @click="alternarGenero(genre.value)"
          >
            {{ genre.label }}
          </button>
        </div>
      </div>

      <div class="filter-section">
        <p class="filter-section-title">Platforms</p>
        <div class="filter-chips">
          <button
            v-for="plat in opcionesDePlataforma"
            :key="plat.value"
            class="filter-chip"
            :class="{ 'is-active': plataformasLocales.includes(plat.value) }"
            @click="alternarPlataforma(plat.value)"
          >
            <i v-if="plat.icon" class="pi" :class="plat.icon"></i>
            {{ plat.label }}
          </button>
        </div>
      </div>

      <div class="filter-section">
        <p class="filter-section-title">Release Year</p>
        <div class="filter-year-range">
          <div class="filter-year-input">
            <label>From</label>
            <input
              type="number"
              v-model.number="fechaDesdeLocal"
              min="1980"
              :max="anioActual"
              placeholder="1980"
            />
          </div>
          <div class="filter-year-sep">—</div>
          <div class="filter-year-input">
            <label>To</label>
            <input
              type="number"
              v-model.number="fechaHastaLocal"
              min="1980"
              :max="anioActual"
              :placeholder="String(anioActual)"
            />
          </div>
        </div>
      </div>

      <div class="filter-actions">
        <button class="filter-btn-clear" @click="manejarLimpiar">
          <i class="pi pi-times"></i>
          Clear filters
        </button>
        <button class="filter-btn-apply" @click="manejarAplicar">
          <i class="pi pi-check"></i>
          Apply filters
        </button>
      </div>

    </div>
  </Transition>
</template>

<script>
// Panel lateral con los filtros del catalogo (orden, generos, plataformas,
// rango de anios). El componente solo mantiene el estado LOCAL mientras
// el usuario va marcando opciones; cuando pulsa "Apply" emite el objeto
// completo al padre con @apply, y este decide cuando recargar la lista.
//
// El panel no se cierra solo: el padre (contenido.vue) lo controla via
// la prop "open".
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
      // Estado interno mientras el usuario configura los filtros.
      // No se sincroniza al padre hasta pulsar "Apply".
      ordenLocal: '',
      generosLocales: [],
      plataformasLocales: [],
      fechaDesdeLocal: '',
      fechaHastaLocal: '',

      // Anio actual para limitar el input "To" y usarlo como placeholder.
      anioActual: new Date().getFullYear(),

      // Opciones disponibles del select de ordenacion (mapeadas al param
      // que espera RAWG en su API).
      opcionesDeOrden: [
        { value: '-rating', label: 'Top Rated', icon: 'pi-star-fill' },
        { value: '-metacritic', label: 'Metacritic', icon: 'pi-chart-bar' },
        { value: 'name', label: 'A–Z', icon: 'pi-sort-alpha-down' },
        { value: '-added', label: 'Popular', icon: 'pi-bolt' }
      ],

      // Lista de generos disponibles. Los "value" son los slugs que usa
      // RAWG; los "label" son los textos que ve el usuario en ingles.
      opcionesDeGenero: [
        { value: 'action', label: 'Action' },
        { value: 'adventure', label: 'Adventure' },
        { value: 'role-playing-games-rpg', label: 'RPG' },
        { value: 'shooter', label: 'Shooter' },
        { value: 'strategy', label: 'Strategy' },
        { value: 'simulation', label: 'Simulation' },
        { value: 'puzzle', label: 'Puzzle' },
        { value: 'sports', label: 'Sports' },
        { value: 'racing', label: 'Racing' },
        { value: 'indie', label: 'Indie' },
        { value: 'casual', label: 'Casual' },
        { value: 'arcade', label: 'Arcade' },
        { value: 'fighting', label: 'Fighting' },
        { value: 'platformer', label: 'Platformer' }
      ],

      // Plataformas mas comunes. El "value" es el id numerico de RAWG.
      opcionesDePlataforma: [
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

    // Selecciona el orden indicado. Si el usuario hace click en el orden
    // que ya estaba activo, lo desactiva (toggle).
    alternarOrden(valor) {
      if (this.ordenLocal === valor) {
        this.ordenLocal = '';
      } else {
        this.ordenLocal = valor;
      }
    },

    // Anade o quita un genero de la seleccion local segun si ya estaba.
    alternarGenero(valor) {
      var indice = this.generosLocales.indexOf(valor);
      if (indice === -1) {
        this.generosLocales.push(valor);
      } else {
        this.generosLocales.splice(indice, 1);
      }
    },

    // Mismo patron que generos pero para plataformas.
    alternarPlataforma(valor) {
      var indice = this.plataformasLocales.indexOf(valor);
      if (indice === -1) {
        this.plataformasLocales.push(valor);
      } else {
        this.plataformasLocales.splice(indice, 1);
      }
    },

    // Construye el objeto de filtros y lo emite al padre.
    // Copiamos los arrays para que el padre no quede atado a nuestro estado interno.
    manejarAplicar() {

      var copiaGeneros = [];
      for (var i = 0; i < this.generosLocales.length; i++) {
        copiaGeneros.push(this.generosLocales[i]);
      }

      var copiaPlataformas = [];
      for (var j = 0; j < this.plataformasLocales.length; j++) {
        copiaPlataformas.push(this.plataformasLocales[j]);
      }

      var fechaDesde = '';
      if (this.fechaDesdeLocal) {
        fechaDesde = this.fechaDesdeLocal;
      }

      var fechaHasta = '';
      if (this.fechaHastaLocal) {
        fechaHasta = this.fechaHastaLocal;
      }

      this.$emit('apply', {
        ordering: this.ordenLocal,
        genres: copiaGeneros,
        platforms: copiaPlataformas,
        dateFrom: fechaDesde,
        dateTo: fechaHasta
      });
    },

    // Resetea el estado local y avisa al padre con @clear.
    manejarLimpiar() {
      this.ordenLocal = '';
      this.generosLocales = [];
      this.plataformasLocales = [];
      this.fechaDesdeLocal = '';
      this.fechaHastaLocal = '';
      this.$emit('clear');
    }
  }
};
</script>

<style scoped src="./FilterPanel.css"></style>
