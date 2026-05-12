import { getContentOverview } from "../../services/resume_cards";
import { getFilteredGames } from "../../services/catalog_filters";
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
            per_page: 20,
            loading: false,
            hasNext: true,
            maxGames: 200,
            showLoadMoreButton: false,
            apiCallCount: 0,
            filterPanelOpen: false,
            filters: {
                ordering: '',
                genres: [],
                platforms: [],
                dateFrom: '',
                dateTo: ''
            }
        }
    },
    computed: {
        hasActiveFilters() {
            const f = this.filters;
            return f.ordering !== '' || f.genres.length > 0 || f.platforms.length > 0 || f.dateFrom !== '' || f.dateTo !== '';
        },
        activeFiltersCount() {
            let count = 0;
            const f = this.filters;
            if (f.ordering) count++;
            count += f.genres.length;
            count += f.platforms.length;
            if (f.dateFrom || f.dateTo) count++;
            return count;
        },
        isFiltering() {
            return this.hasActiveFilters || !!this.game_name;
        }
    },
    mounted() {
        if (this.$route.query.q) {
            this.game_name = this.$route.query.q;
        }
        if (this.isFiltering) {
            this.getFilteredContent();
        } else {
            this.getContent();
            this.debouncedScroll = this.debounce(this.handleScroll, 500);
            window.addEventListener("scroll", this.debouncedScroll);
        }
        document.addEventListener('mousedown', this.handleFilterClickOutside);
    },
    beforeUnmount() {
        if (this.debouncedScroll) {
            window.removeEventListener("scroll", this.debouncedScroll);
        }
        document.removeEventListener('mousedown', this.handleFilterClickOutside);
    },
    watch: {
        '$route.query.q'(newVal) {
            this.game_name = newVal || null;
            this.resetCatalog();

            if (this.debouncedScroll) {
                window.removeEventListener("scroll", this.debouncedScroll);
                this.debouncedScroll = null;
            }

            if (this.isFiltering) {
                this.getFilteredContent();
            } else {
                this.debouncedScroll = this.debounce(this.handleScroll, 500);
                window.addEventListener("scroll", this.debouncedScroll);
                this.getContent();
            }
        }
    },

    methods: {
        resetCatalog() {
            this.games = [];
            this.page = 1;
            this.hasNext = true;
            this.apiCallCount = 0;
            this.showLoadMoreButton = false;
            this.favorites = new Set();
        },

        async getContent() {
            if (this.loading || !this.hasNext || this.games.length >= this.maxGames) return;
            this.loading = true;
            try {
                const response = await getContentOverview(this.page, null);
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

        async getFilteredContent() {
            if (this.loading || !this.hasNext) return;
            this.loading = true;
            try {
                const response = await getFilteredGames(this.page, this.per_page, {
                    ...this.filters,
                    search: this.game_name || ''
                });
                this.games = [...this.games, ...response.games];
                for (const game of response.games) {
                    await this.initCheckFavorite(game.id);
                }
                this.hasNext = !!response.next;
                this.page++;
                this.showLoadMoreButton = this.hasNext;
            } catch (error) {
                console.error("Error en catálogo filtrado:", error);
                this.games = [];
            } finally {
                this.loading = false;
            }
        },

        applyFilters(newFilters) {
            this.filters = { ...newFilters };
            this.filterPanelOpen = false;
            this.resetCatalog();
            if (this.debouncedScroll) {
                window.removeEventListener("scroll", this.debouncedScroll);
                this.debouncedScroll = null;
            }
            if (this.isFiltering) {
                this.getFilteredContent();
            } else {
                this.debouncedScroll = this.debounce(this.handleScroll, 500);
                window.addEventListener("scroll", this.debouncedScroll);
                this.getContent();
            }
        },

        clearFilters() {
            this.filters = { ordering: '', genres: [], platforms: [], dateFrom: '', dateTo: '' };
            this.filterPanelOpen = false;
            this.resetCatalog();
            if (this.debouncedScroll) {
                window.removeEventListener("scroll", this.debouncedScroll);
                this.debouncedScroll = null;
            }
            if (this.game_name) {
                this.getFilteredContent();
            } else {
                this.debouncedScroll = this.debounce(this.handleScroll, 500);
                window.addEventListener("scroll", this.debouncedScroll);
                this.getContent();
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

        handleFilterClickOutside(e) {
            if (!this.filterPanelOpen) return;
            if (e.target.closest('.filter-panel') || e.target.closest('.filter-toggle-btn')) return;
            this.filterPanelOpen = false;
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
            if (this.isFiltering) {
                this.getFilteredContent();
            } else {
                this.getContent();
            }
        },

        goToDetail(gameId) {
            this.$router.push(`/game/${gameId}`);
        },

        debounce(fn, delay) {
            let timer = null;
            return function (...args) {
                clearTimeout(timer);
                timer = setTimeout(() => fn.apply(this, args), delay);
            }
        }
    }
}
