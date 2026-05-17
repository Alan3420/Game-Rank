import { getFilteredGames } from "../../services/catalog_filters";
import { getCatalogGames } from "../../services/resume_cards";
import { addTOFavorite, checkFavorite, removeTOFavorite } from "../../services/favorites_area";
import { listGameStatuses } from "../../services/user_game_status";
import { notificaciones } from "../../store/notificaciones";
import { estadoAutenticacion } from "../../store/autenticacion";

const PER_PAGE = 20;

export default {
    name: "contenido",
    data() {
        return {
            games: [],
            favorites: new Set(),
            statuses: new Map(),
            game_name: null,
            currentPage: 1,
            totalCount: 0,
            loading: false,
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
        },
        totalPages() {
            if (!this.totalCount) return 0;
            // RAWG stops serving results past ~500 pages regardless of count
            return Math.min(Math.ceil(this.totalCount / PER_PAGE), 500);
        },
        paginasVisibles() {
            const total = this.totalPages;
            const current = this.currentPage;

            if (total <= 7) {
                return Array.from({ length: total }, (_, i) => i + 1);
            }

            const pages = new Set([1, total]);
            for (let i = Math.max(2, current - 2); i <= Math.min(total - 1, current + 2); i++) {
                pages.add(i);
            }

            const sorted = [...pages].sort((a, b) => a - b);
            const result = [];
            for (let i = 0; i < sorted.length; i++) {
                if (i > 0 && sorted[i] - sorted[i - 1] > 1) {
                    result.push('...');
                }
                result.push(sorted[i]);
            }
            return result;
        }
    },
    async mounted() {
        if (this.$route.query.q) {
            this.game_name = this.$route.query.q;
        }
        const initialPage = Math.min(parseInt(this.$route.query.page) || 1, 500);
        await this.fetchPage(initialPage);
        document.addEventListener('mousedown', this.handleFilterClickOutside);
        if (estadoAutenticacion.usuario) {
            await this.loadStatuses();
        }
    },
    beforeUnmount() {
        document.removeEventListener('mousedown', this.handleFilterClickOutside);
    },
    watch: {
        '$route.query.page'(newVal) {
            const page = Math.min(parseInt(newVal) || 1, 500);
            if (page !== this.currentPage) {
                this.fetchPage(page);
            }
        },
        async '$route.query.q'(newVal) {
            this.game_name = newVal || null;
            await this.fetchPage(1);
        }
    },

    methods: {
        async fetchPage(page) {
            this.loading = true;
            this.currentPage = page;

            const query = { ...this.$route.query };
            if (page > 1) {
                query.page = page;
            } else {
                delete query.page;
            }
            this.$router.replace({ query });

            try {
                const response = this.isFiltering
                    ? await getFilteredGames(page, PER_PAGE, { ...this.filters, search: this.game_name || '' })
                    : await getCatalogGames(page, PER_PAGE);
                this.games = response.games ?? [];
                this.totalCount = response.count ?? 0;

                if (this.totalPages > 0 && page > this.totalPages) {
                    await this.fetchPage(this.totalPages);
                    return;
                }

                // Mostrar juegos inmediatamente sin esperar a favoritos
                this.loading = false;

                // Comprobar favoritos en paralelo en segundo plano (solo si hay sesión)
                if (estadoAutenticacion.usuario) {
                    this.favorites = new Set();
                    await Promise.all(this.games.map(g => this.initCheckFavorite(g.id)));
                }
            } catch (error) {
                console.error(error);
                this.games = [];
                this.loading = false;
            }
        },

        async loadStatuses() {
            try {
                const data = await listGameStatuses();
                const map = new Map();
                for (const s of data.statuses) {
                    map.set(s.id_game_api, s.status);
                }
                this.statuses = map;
            } catch {
                // fallo silencioso
            }
        },

        handleStatusUpdate({ gameId, status }) {
            const map = new Map(this.statuses);
            if (status) {
                map.set(gameId, status);
            } else {
                map.delete(gameId);
            }
            this.statuses = map;
        },

        applyFilters(newFilters) {
            this.filters = { ...newFilters };
            this.filterPanelOpen = false;
            this.fetchPage(1);
        },

        clearFilters() {
            this.filters = { ordering: '', genres: [], platforms: [], dateFrom: '', dateTo: '' };
            this.filterPanelOpen = false;
            this.fetchPage(1);
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

        goToDetail(gameId) {
            this.$router.push(`/game/${gameId}`);
        }
    }
}
