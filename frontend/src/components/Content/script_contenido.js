import { obtenerJuegosFiltrados } from "../../services/catalog_filters";
import { obtenerJuegosDelCatalogo } from "../../services/resume_cards";
import { agregarAFavoritos, consultarSiEsFavorito, quitarDeFavoritos } from "../../services/favorites_area";
import { listarEstadosDeJuego } from "../../services/user_game_status";
import { notificaciones } from "../../store/notificaciones";
import { estadoAutenticacion } from "../../store/autenticacion";
import { STATUS_META } from "../../utils/statusMeta.js";
import { claseMetacritic } from "../../utils/metacritic.js";
import { formatearFechaCorta } from "../../utils/formatoFecha.js";

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
            STATUS_META,
            // "grid" (album de cartas) o "checklist" (tabla del set); vive
            // en la URL (?view=checklist) para poder compartirlo
            vista: 'grid',
            // en movil la barra de filtros se despliega como cajon
            filtrosAbiertos: false,
            // id del juego cuyo menu de estado esta abierto en la checklist
            menuEstadoAbierto: null,
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

        titulo() {
            if (this.game_name) {
                return 'Results for "' + this.game_name + '"';
            }
            if (this.tieneFiltrosActivos) {
                return 'Filtered catalog';
            }
            return 'Game catalog';
        },

        etiquetaOrden() {
            var nombres = {
                '': 'relevance',
                '-rating': 'top rated',
                '-metacritic': 'Metacritic, high to low',
                'metacritic': 'Metacritic, low to high',
                '-released': 'newest',
                'released': 'oldest',
                'name': 'name, A to Z',
                '-name': 'name, Z to A',
                '-added': 'popularity'
            };
            var etiqueta = nombres[this.filters.ordering];
            return etiqueta || 'relevance';
        },

        textoTotal() {
            if (!this.totalCount) {
                return 'No games';
            }
            var total = Number(this.totalCount).toLocaleString('en');
            return total + (this.totalCount === 1 ? ' game' : ' games');
        },

        tieneFiltrosActivos() {
            var f = this.filters;
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

            total = total + f.genres.length;
            total = total + f.platforms.length;
            // El rango de fechas cuenta como uno, no como dos
            if (f.dateFrom || f.dateTo) {
                total = total + 1;
            }
            return total;
        },

        // Usa el endpoint de filtros si hay filtros, busqueda o un orden
        // distinto del de por defecto (el orden no cuenta como filtro)
        estaFiltrando() {
            if (this.tieneFiltrosActivos || this.filters.ordering) {
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
        if (this.$route.query.view === 'checklist') {
            this.vista = 'checklist';
        }

        var paginaInicial = parseInt(this.$route.query.page);
        if (!paginaInicial || isNaN(paginaInicial)) {
            paginaInicial = 1;
        }
        if (paginaInicial > 500) {
            paginaInicial = 500;
        }

        await this.cargarPagina(paginaInicial);

        document.addEventListener('mousedown', this.cerrarMenuEstadoSiFuera);

        if (this.haySesion()) {
            await this.cargarEstadosDeColeccion();
        }
    },

    beforeUnmount() {
        document.removeEventListener('mousedown', this.cerrarMenuEstadoSiFuera);
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
                consulta[clave] = this.$route.query[clave];
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

                if (this.haySesion()) {
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
            this.filtrosAbiertos = false;
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
            this.filtrosAbiertos = false;
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

                var mensaje = "Game wasn't added to favorites. Check your connection and try again.";
                if (eraFavorito) {
                    mensaje = "Game wasn't removed from favorites. Check your connection and try again.";
                }
                notificaciones.error(mensaje, { title: "Favorites error" });
            }
        },

        claseMetacritic,

        // Al entrar directo por URL la sesion aun se esta restaurando y
        // estadoAutenticacion.usuario llega tarde: el token ya basta
        haySesion() {
            return !!(estadoAutenticacion.usuario || localStorage.getItem('token'));
        },

        formatearFecha(valor) {
            return formatearFechaCorta(valor);
        },

        // Un juego que aun no ha salido no puede estar "jugando" ni
        // "completado": el estado solo se ofrece a favoritos ya lanzados
        juegoYaSalio(juego) {
            if (!juego.release_date) {
                return false;
            }
            return new Date(juego.release_date + 'T00:00:00') <= new Date();
        },

        puedeCambiarEstado(juego) {
            return this.favorites.has(juego.id) && this.juegoYaSalio(juego);
        },

        cambiarVista(nueva) {
            this.vista = nueva;
            var consulta = {};
            for (var clave in this.$route.query) {
                consulta[clave] = this.$route.query[clave];
            }
            if (nueva === 'checklist') {
                consulta.view = 'checklist';
            } else {
                delete consulta.view;
            }
            this.$router.replace({ query: consulta });
        },

        // Orden desde la cabecera de la checklist: alterna descendente y
        // ascendente sobre la misma columna (RAWG acepta "campo"/"-campo")
        ordenarPor(campo) {
            var actual = this.filters.ordering;
            var nuevo;
            if (campo === 'name') {
                nuevo = actual === 'name' ? '-name' : 'name';
            } else {
                nuevo = actual === '-' + campo ? campo : '-' + campo;
            }
            this.filters = Object.assign({}, this.filters, { ordering: nuevo });
            this.cargarPagina(1);
        },

        ariaSort(campo) {
            var actual = this.filters.ordering;
            if (actual === campo) {
                return 'ascending';
            }
            if (actual === '-' + campo) {
                return 'descending';
            }
            return 'none';
        },

        alternarMenuEstado(gameId) {
            this.menuEstadoAbierto = this.menuEstadoAbierto === gameId ? null : gameId;
        },

        cerrarMenuEstadoSiFuera(evento) {
            if (this.menuEstadoAbierto === null) {
                return;
            }
            if (evento.target.closest('.cat-row__status')) {
                return;
            }
            this.menuEstadoAbierto = null;
        },

        irADetalle(gameId) {
            this.$router.push('/game/' + gameId);
        }
    }
};
