<template>
  <img
    :src="currentImage"
    :alt="alt"
    :class="imageClass"
    @error="handleImageError"
  />
</template>

<script>
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
    return {
      currentImage: this.src || placeholder,
      defaultImage: placeholder
    };
  },
  watch: {
    src(newVal) {
      if (newVal) {
        this.currentImage = newVal;
      }
    }
  },
  methods: {
    handleImageError() {
      if (this.currentImage !== this.defaultImage) {
        this.currentImage = this.defaultImage;
      }
    }
  }
};
</script>
