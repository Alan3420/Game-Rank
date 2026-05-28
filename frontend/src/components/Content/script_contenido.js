import { obtenerJuegosFiltrados } from "../../services/catalog_filters";
import { obtenerJuegosDelCatalogo } from "../../services/resume_cards";
import { agregarAFavoritos, consultarSiEsFavorito, quitarDeFavoritos } from "../../services/favorites_area";
import { listarEstadosDeJuego } from "../../services/user_game_status";
import { notificaciones } from "../../store/notificaciones";
import { estadoAutenticacion } from "../../store/autenticacion";

const POR_PAGINA = 20;


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
        };
    },

    computed: {

        tieneFiltrosActivos() {
            var f = this.filters;
            if (f.ordering !== '') {
                return true;
            }
            if (f.genres.length > 0) {
                return true;
            }
            if (f.platforms.length > 0) {
                return true;
            }
            if (f.dateFrom !== '' || f.dateTo !== '') {
                return true;
            }
            return false;
        },

        cantidadFiltrosActivos() {
            var total = 0;
            var f = this.filters;

            if (f.ordering) {
                total = total + 1;
            }
            total = total + f.genres.length;
            total = total + f.platforms.length;
            // El rango de fechas cuenta como uno, no como dos
            if (f.dateFrom || f.dateTo) {
                total = total + 1;
            }
            return total;
        },

        estaFiltrando() {
            if (this.tieneFiltrosActivos) {
                return true;
            }
            if (this.game_name) {
                return true;
            }
            return false;
        },

        // Tope de 500 paginas porque RAWG corta ahi aunque el count diga mas,
        // si dejamos pasar paginas mas altas saldria lista vacia
        totalPaginas() {
            if (!this.totalCount) {
                return 0;
            }
            var calculado = Math.ceil(this.totalCount / POR_PAGINA);
            if (calculado > 500) {
                return 500;
            }
            return calculado;
        }
    },

    async mounted() {

        if (this.$route.query.q) {
            this.game_name = this.$route.query.q;
        }

        var paginaInicial = parseInt(this.$route.query.page);
        if (!paginaInicial || isNaN(paginaInicial)) {
            paginaInicial = 1;
        }
        if (paginaInicial > 500) {
            paginaInicial = 500;
        }

        await this.cargarPagina(paginaInicial);

        document.addEventListener('mousedown', this.manejarClicFueraDeFiltros);

        if (estadoAutenticacion.usuario) {
            await this.cargarEstadosDeColeccion();
        }
    },

    beforeUnmount() {
        document.removeEventListener('mousedown', this.manejarClicFueraDeFiltros);
    },

    watch: {

        '$route.query.page'(nuevoValor) {
            var pagina = parseInt(nuevoValor);
            if (!pagina || isNaN(pagina)) {
                pagina = 1;
            }
            if (pagina > 500) {
                pagina = 500;
            }
            if (pagina !== this.currentPage) {
                this.cargarPagina(pagina);
            }
        },

        async '$route.query.q'(nuevoValor) {
            if (nuevoValor) {
                this.game_name = nuevoValor;
            } else {
                this.game_name = null;
            }
            await this.cargarPagina(1);
        }
    },

    methods: {

        async cargarPagina(pagina) {

            this.loading = true;
            this.currentPage = pagina;

            // Reflejamos la pagina en la URL para que se mantenga al
            // recargar o al compartir el enlace
            var consulta = {};
            for (var clave in this.$route.query) {
                if (Object.prototype.hasOwnProperty.call(this.$route.query, clave)) {
                    consulta[clave] = this.$route.query[clave];
                }
            }
            if (pagina > 1) {
                consulta.page = pagina;
            } else {
                delete consulta.page;
            }
            this.$router.replace({ query: consulta });

            try {

                var respuesta = null;

                if (this.estaFiltrando) {
                    var filtrosCompletos = {
                        ordering: this.filters.ordering,
                        genres: this.filters.genres,
                        platforms: this.filters.platforms,
                        dateFrom: this.filters.dateFrom,
                        dateTo: this.filters.dateTo,
                        search: this.game_name || ''
                    };
                    respuesta = await obtenerJuegosFiltrados(pagina, POR_PAGINA, filtrosCompletos);
                } else {
                    respuesta = await obtenerJuegosDelCatalogo(pagina, POR_PAGINA);
                }

                if (respuesta.games) {
                    this.games = respuesta.games;
                } else {
                    this.games = [];
                }

                if (respuesta.count) {
                    this.totalCount = respuesta.count;
                } else {
                    this.totalCount = 0;
                }

                if (this.totalPaginas > 0 && pagina > this.totalPaginas) {
                    await this.cargarPagina(this.totalPaginas);
                    return;
                }

                // Mostramos el grid enseguida y dejamos los favoritos
                // cargandose por detras para que la UI no espere
                this.loading = false;

                if (estadoAutenticacion.usuario) {
                    this.favorites = new Set();
                    var tareas = [];
                    for (var i = 0; i < this.games.length; i++) {
                        tareas.push(this.comprobarFavoritoInicial(this.games[i].id));
                    }
                    await Promise.all(tareas);
                }

            } catch (error) {
                console.error(error);
                this.games = [];
                this.loading = false;
            }
        },

        async cargarEstadosDeColeccion() {
            try {
                var data = await listarEstadosDeJuego();
                var mapa = new Map();
                for (var i = 0; i < data.statuses.length; i++) {
                    mapa.set(data.statuses[i].id_game_api, data.statuses[i].status);
                }
                this.statuses = mapa;
            } catch (error) {
            }
        },

        manejarActualizacionEstado(datos) {
            var gameId = datos.gameId;
            var status = datos.status;

            var mapa = new Map(this.statuses);
            if (status) {
                mapa.set(gameId, status);
            } else {
                mapa.delete(gameId);
            }
            this.statuses = mapa;
        },

        aplicarFiltros(nuevosFiltros) {
            this.filters = {
                ordering: nuevosFiltros.ordering,
                genres: nuevosFiltros.genres,
                platforms: nuevosFiltros.platforms,
                dateFrom: nuevosFiltros.dateFrom,
                dateTo: nuevosFiltros.dateTo
            };
            this.filterPanelOpen = false;
            this.cargarPagina(1);
        },

        limpiarFiltros() {
            this.filters = {
                ordering: '',
                genres: [],
                platforms: [],
                dateFrom: '',
                dateTo: ''
            };
            this.filterPanelOpen = false;
            this.cargarPagina(1);
        },

        async comprobarFavoritoInicial(gameId) {
            try {
                var data = await consultarSiEsFavorito(gameId);
                if (data.is_favorite) {
                    this.favorites.add(gameId);
                }
            } catch (error) {
                console.error('Error verificando favorito ' + gameId + ':', error);
            }
        },

        async alternarFavorito(gameId) {

            var eraFavorito = this.favorites.has(gameId);

            try {
                if (eraFavorito) {
                    await quitarDeFavoritos(gameId);
                    this.favorites.delete(gameId);
                    notificaciones.success("Game removed from your favorites.", { title: "Favorite removed" });
                } else {
                    await agregarAFavoritos(gameId);
                    this.favorites.add(gameId);
                    notificaciones.success("Game added to your favorites.", { title: "Favorite added" });
                }
            } catch (error) {
                console.error("Error al cambiar favorito:", error);

                var mensaje = "We couldn't add the game to favorites.";
                if (eraFavorito) {
                    mensaje = "We couldn't remove the game from favorites.";
                }
                notificaciones.error(mensaje, { title: "Favorites error" });
            }
        },

        manejarClicFueraDeFiltros(e) {
            if (!this.filterPanelOpen) {
                return;
            }
            if (e.target.closest('.filter-panel')) {
                return;
            }
            if (e.target.closest('.filter-toggle-btn')) {
                return;
            }
            this.filterPanelOpen = false;
        },

        irADetalle(gameId) {
            this.$router.push('/game/' + gameId);
        }
    }
};
