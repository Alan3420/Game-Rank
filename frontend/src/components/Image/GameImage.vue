<template>
  <img
    :src="imagenActual"
    :alt="alt"
    :class="imageClass"
    @error="cuandoFallaLaImagen"
  />
</template>

<script>
// Imagen con fallback. Si la URL pasada en "src" falla al cargar (404, CORS,
// etc.) cambia automaticamente al SVG placeholder. Asi evitamos cards
// rotas en el catalogo cuando RAWG no devuelve imagen valida.
import placeholder from '../../assets/game-placeholder.svg';

export default {
  name: 'GameImage',

  props: {
    src: {
      type: String,
      required: true
    },
    alt: {
      type: String,
      default: 'Game Image'
    },
    imageClass: {
      type: String,
      default: ''
    }
  },

  data() {
    var imagenInicial = '';
    if (this.src) {
      imagenInicial = this.src;
    } else {
      imagenInicial = placeholder;
    }

    return {
      imagenActual: imagenInicial,
      imagenPorDefecto: placeholder
    };
  },

  watch: {
    // Si el padre cambia el "src" (por ejemplo al navegar a otro juego)
    // reseteamos la imagen para intentar la nueva URL.
    src(nuevoValor) {
      if (nuevoValor) {
        this.imagenActual = nuevoValor;
      }
    }
  },

  methods: {
    // Listener del evento "error" de la etiqueta <img>. Solo cambiamos al
    // placeholder si no estabamos ya en el, para evitar bucles infinitos
    // en el caso (raro) de que el propio placeholder fallara.
    cuandoFallaLaImagen() {
      if (this.imagenActual !== this.imagenPorDefecto) {
        this.imagenActual = this.imagenPorDefecto;
      }
    }
  }
};
</script>
