import { getContentOverview, getHeroVideo } from '../../services/resume_cards.js';
import { getFutureReleases } from '../../services/clasif_content.js';
import { estadoAutenticacion } from '../../store/autenticacion.js';
import { checkFavorite, addTOFavorite, removeTOFavorite } from '../../services/favorites_area.js';
import { notificaciones } from '../../store/notificaciones.js';
import { computed } from 'vue';

export default {
  name: "home",
  data() {
    return {
      topGames: [],
      futureReleases: [],
      favorites: new Set(),
      carouselTrack: null,
      isLoading: true,
      isFutureLoading: true,
      heroVideo: null
    };
  },
  async mounted() {
    await this.loadHeroVideo();

    if (!localStorage.getItem("token")) return;

    if (this.topGames.length === 0) {
      await this.loadTopGames();
    }
    if (this.futureReleases.length === 0) {
      await this.loadFutureReleases();
    }
  },
  methods: {
    async loadHeroVideo() {
      try {
        const video = await getHeroVideo();
        this.heroVideo = video || null;
      } catch (error) {
        console.error('Error al cargar video del hero:', error);
        this.heroVideo = null;
      }
    },

    async loadTopGames() {
      this.isLoading = true;
      try {
        const response = await getContentOverview(1);

        let games = [];
        if (response && response.games && Array.isArray(response.games)) {
          games = response.games;
        } else if (Array.isArray(response)) {
          games = response;
        }

        const validGames = games.filter(game => game.rating && game.rating > 0);

        const sorted = validGames.sort((a, b) => b.rating - a.rating);
        this.topGames = sorted.slice(0, 3);

        for (const game of this.topGames) {
          await this.initCheckFavorite(game.id);
        }

      } catch (error) {
        console.error('Error loading top games:', error);
      } finally {
        this.isLoading = false;
      }
    },

    async loadFutureReleases() {
      try {
        const response = await getFutureReleases(1, 10);
        this.futureReleases = response || [];

        for (const game of this.futureReleases) {
          await this.initCheckFavorite(game.id);
        }
      } catch (error) {
        console.error('Error loading future releases:', error);
      } finally {
        this.isFutureLoading = false;
      }
    },

    async initCheckFavorite(gameId) {
      try {
        const data = await checkFavorite(gameId);
        if (data.is_favorite) {
          this.favorites.add(gameId);
        }
      } catch (error) {
        console.error(`Error verificando favorito ${gameId}:`, error);
      }
    },

    async toggleFavorite(gameId) {
      const wasFavorite = this.favorites.has(gameId);
      try {
        if (wasFavorite) {
          await removeTOFavorite(gameId);
          this.favorites.delete(gameId);
          notificaciones.success("Juego eliminado de tus favoritos.", { title: "Favorito eliminado" });
        } else {
          await addTOFavorite(gameId);
          this.favorites.add(gameId);
          notificaciones.success("Juego añadido a tus favoritos.", { title: "Favorito agregado" });
        }
      } catch (error) {
        console.error("Error al cambiar favorito:", error);
        notificaciones.error(
          wasFavorite
            ? "No pudimos eliminar el juego de favoritos."
            : "No pudimos añadir el juego a favoritos.",
          { title: "Error en favoritos" }
        );
      }
    },

    goToDetail(gameId) {
      this.$router.push(`/game/${gameId}`);
    },

    // scrollCarousel(dir) {
    //   const track = this.$refs.carouselTrack;
    //   if (track) track.scrollBy({ left: dir * 300, behavior: 'smooth' });
    // },

    goToLogin() {
      const token = localStorage.getItem("token")
      if (token) {
        this.$router.push('/content/overview');
      } else {
        this.$router.push('/login');
      }
    },


    goToRegister() {
      this.$router.push("/register");
    },

    goToExplore() {
      this.$router.push('/content/overview');
    },

    scrollToReleases() {
      const element = document.getElementById('proximos-section');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  },
  computed: {
    estadoAutenticacion() {
      return estadoAutenticacion;
    }
  }
}

