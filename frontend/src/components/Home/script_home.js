import { getContentOverview } from '../../services/resume_cards.js';
import { getFutureReleases } from '../../services/clasif_content.js';
import { estadoAutenticacion } from '../../store/autenticacion.js';
import { computed } from 'vue';

export default {
  name: "home",
  data() {
    return {
      topGames: [],
      futureReleases: [],
      carouselTrack: null,
      isLoading: false
    };
  },
  async mounted() {
    if (this.topGames.length === 0) {
      await this.loadTopGames();
    }
    if (this.futureReleases.length === 0) {
      await this.loadFutureReleases();
    }
  },
  methods: {
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

      } catch (error) {
        console.error('Error loading top games:', error);
      } finally {
        this.isLoading = false;
      }
    },

    async loadFutureReleases() {
      try {
        const response = await getFutureReleases(1, 10);
        console.log(response);

        this.futureReleases = response || [];
      } catch (error) {
        console.error('Error loading future releases:', error);
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
    }
  },
  computed: {
    estadoAutenticacion() {
      return estadoAutenticacion;
    }
  }
}

