import { getContentOverview } from "../../services/resume_cards";
import { getContentByName } from "../../services/buscar"
import { addTOFavorite, checkFavorite, removeTOFavorite } from "../../services/favorites_area";
import { notificaciones } from "../../store/notificaciones";

export default {
    name: "contenido",
    data() {
        return {
            games: [],
            favorites: new Set(),
            game_name: null,
            page: 1,
            per_page: 10,
            loading: false,
            hasNext: true,
            maxGames: 200,
            showLoadMoreButton: false,
            apiCallCount: 0
        }
    },
    mounted() {
        if (this.$route.query.q) {
            this.game_name = this.$route.query.q;
            this.searchGames();
        } else {
            this.getContent();
            this.debouncedScroll = this.debounce(this.handleScroll, 500)
            window.addEventListener("scroll", this.debouncedScroll);
        }
    },
    beforeUnmount() {
        if (this.debouncedScroll) {
            window.removeEventListener("scroll", this.debouncedScroll);
        }
    },
    watch: {
        '$route.query.q'(newVal) {
            this.game_name = newVal || null;
            this.games = [];
            this.page = 1;
            this.hasNext = true;
            this.apiCallCount = 0;
            this.showLoadMoreButton = false;
            this.favorites = new Set();

            if (this.debouncedScroll) {
                window.removeEventListener("scroll", this.debouncedScroll);
            }

            if (this.game_name) {
                this.searchGames();
            } else {
                this.debouncedScroll = this.debounce(this.handleScroll, 500);
                window.addEventListener("scroll", this.debouncedScroll);
                this.getContent();
            }
        }
    },


    methods: {
        async getContent() {
            if (this.loading || !this.hasNext || this.games.length >= this.maxGames) return;

            this.loading = true;

            try {
                const response = await getContentOverview(this.page, this.game_name);

                this.games = [...this.games, ...response.games];

                for (const game of response.games) {
                    await this.initCheckFavorite(game.id);
                }

                this.hasNext = !!response.next;

                this.page++;
                this.apiCallCount++;

                if (this.apiCallCount >= 2) {
                    this.showLoadMoreButton = true;
                    window.removeEventListener("scroll", this.debouncedScroll);
                }

            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;
            }
        },

        async searchGames() {
            if (this.loading) return;
            this.loading = true;
            try {
                const response = await getContentByName(this.game_name);
                this.games = Array.isArray(response) ? response : [];
                this.hasNext = false;
                this.showLoadMoreButton = false;

                for (const game of this.games) {
                    await this.initCheckFavorite(game.id);
                }
            } catch (error) {
                console.error("Error en búsqueda:", error);
                this.games = [];
            } finally {
                this.loading = false;
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

        handleScroll() {
            const scrollTop = window.scrollY;
            const windowHeight = window.innerHeight;
            const fullHeight = document.documentElement.scrollHeight;


            if (this.apiCallCount < 2 && scrollTop + windowHeight >= fullHeight - 1000) {
                this.getContent();
            }
        },

        loadMore() {
            this.getContent();
        },

        goToDetail(gameId) {
            this.$router.push(`/game/${gameId}`);
        },

        debounce(fn, delay) {
            let timer = null
            return function (...args) {
                clearTimeout(timer)
                timer = setTimeout(() => fn.apply(this, args), delay)
            }
        }
    }
}
