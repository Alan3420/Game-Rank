import { getContentOverview } from '../../services/resume_cards.js';

export default {
    name: "home",
  data() {
    return {
      topGames: [],
      isLoading: true
    };
  },
  async mounted() {
    await this.loadTopGames();
  },
  methods: {
    async loadTopGames() {
      this.isLoading = true;
      try {
        const response = await getContentOverview(1);
        console.log('API Response:', response);
        
        let games = [];
        if (response && response.games && Array.isArray(response.games)) {
          games = response.games;
        } else if (Array.isArray(response)) {
          games = response;
        }
        
        const validGames = games.filter(game => game.rating && game.rating > 0);
        console.log('Valid games found:', validGames.length);
        
        const sorted = validGames.sort((a, b) => b.rating - a.rating);
        this.topGames = sorted.slice(0, 3);
        console.log('Top 3 games:', this.topGames);
      } catch (error) {
        console.error('Error loading top games:', error);
      } finally {
        this.isLoading = false;
      }
    },
    goToLogin() {
      const token = localStorage.getItem("token")
      if (token) {
        this.$router.push('/content/overview');
      } else {
        this.$router.push('/login');
      }
    },
    goToRegister(){
      this.$router.push("/register");
    }
  }
}

