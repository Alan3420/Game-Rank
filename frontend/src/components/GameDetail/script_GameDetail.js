import { obtenerDetalleDeJuego, obtenerSagaDelJuego, obtenerAdiccionesJuego, obtenerLogrosJuego } from '../../services/gameDetail';
import { obtenerComentariosDelJuego, crearComentario, eliminarComentario, actualizarComentario, obtenerPromedioDeCalificacion } from '../../services/comment_services';
import { agregarAFavoritos, quitarDeFavoritos, consultarSiEsFavorito, obtenerEstadoDeJuego } from '../../services/favorites_area';
import { estadoAutenticacion } from '../../store/autenticacion';
import { notificaciones } from '../../store/notificaciones';
import { STATUS_META } from '../../utils/statusMeta.js';
import DOMPurify from 'dompurify';


export default {
    name: 'GameDetail',

    data() {
        return {
            game: null,
            screenshots: [],
            loading: true,
            activeShot: 0,
            errorMessage: '',
            comments: [],
            totalComments: 0,
            hasMoreComments: false,
            loadingMore: false,
            newComment: '',
            editingId: null,
            editDescription: '',
            isFavorite: false,
            favoriteLoading: false,
            sagaFavoritos: new Set(),
            formRating: 0,
            formHover: 0,
            communityAvg: 0,
            gameStatus: null,
            showStatusModal: false,
            STATUS_META: STATUS_META,
            juegosSaga: [],
            adiciones: [],
            logros: [],
            externalLink: {
                open: false,
                url: '',
                storeName: ''
            }
        };
    },

    computed: {

        data_user() {
            return estadoAutenticacion.usuario;
        },

        // Limpiamos el HTML de la descripcion con DOMPurify antes de meterlo
        // con v-html, asi cortamos cualquier intento de XSS
        descripcionSanitizada() {
            var html = '';
            if (this.game && this.game.description) {
                html = this.game.description;
            }
            return DOMPurify.sanitize(html);
        },

        // No tiene sentido dejar marcar como "jugando" un juego que aun no salio
        juegoYaSalio() {
            if (!this.game || !this.game.release_date) {
                return false;
            }
            // Como las fechas vienen en ISO YYYY-MM-DD podemos comparar
            // strings directamente, el orden alfabetico coincide con el cronologico
            var hoy = new Date();
            var anio = hoy.getFullYear();
            var mes = hoy.getMonth() + 1;
            var dia = hoy.getDate();

            var mesTexto = '';
            if (mes < 10) {
                mesTexto = '0' + mes;
            } else {
                mesTexto = '' + mes;
            }

            var diaTexto = '';
            if (dia < 10) {
                diaTexto = '0' + dia;
            } else {
                diaTexto = '' + dia;
            }

            var hoyIso = anio + '-' + mesTexto + '-' + diaTexto;
            return this.game.release_date <= hoyIso;
        },

        hasOwnComment() {
            if (!this.data_user) {
                return false;
            }
            for (var i = 0; i < this.comments.length; i++) {
                if (this.comments[i].id_user === this.data_user.id_user) {
                    return true;
                }
            }
            return false;
        },

        formularioDeshabilitado() {
            if (this.hasOwnComment && !this.editingId) {
                return true;
            }
            return false;
        },

        // Mezclamos trailers y capturas en una sola lista para que la
        // galeria pueda iterar como si fueran lo mismo
        mediaItems() {

            var resultado = [];

            if (this.game && this.game.movies) {
                for (var i = 0; i < this.game.movies.length; i++) {
                    var m = this.game.movies[i];
                    resultado.push({
                        type: 'video',
                        url: m.trailer_url,
                        name: m.name,
                        preview: m.preview
                    });
                }
            }

            if (this.game && this.game.screenshots) {
                for (var j = 0; j < this.game.screenshots.length; j++) {
                    var s = this.game.screenshots[j];
                    resultado.push({
                        type: 'image',
                        url: s.image
                    });
                }
            }

            return resultado;
        }
    },

    async mounted() {
        window.scrollTo({ top: 0, left: 0, behavior: 'auto' });

        await this.cargarDetalleDelJuego();
        await this.cargarComentarios();
        await this.cargarPromedioDeComunidad();
        await this.comprobarSiEsFavorito();
        await this.cargarEstadoDelJuego();

        var self = this;
        this.cargarSagaDelJuego().then(function() {
            self.cargarFavoritosDeSaga();
        });
        this.cargarAdiciones();
        this.cargarLogros();
    },

    watch: {

        // Al ir de /game/1 a /game/2 Vue no destruye el componente, asi que
        // hay que recargar todo a mano y resetear primero para no mostrar
        // los datos del juego anterior mientras llega la peticion
        '$route.params.id'(nuevoId, viejoId) {

            if (!nuevoId || nuevoId === viejoId) {
                return;
            }

            window.scrollTo({ top: 0, left: 0, behavior: 'auto' });

            this.formRating = 0;
            this.formHover = 0;
            this.editingId = null;
            this.newComment = '';
            this.gameStatus = null;
            this.showStatusModal = false;
            this.juegosSaga = [];
            this.sagaFavoritos = new Set();
            this.adiciones = [];
            this.logros = [];
            this.comments = [];
            this.totalComments = 0;
            this.hasMoreComments = false;

            var self = this;
            this.cargarDetalleDelJuego(nuevoId).then(function () {
                self.cargarComentarios();
                self.cargarPromedioDeComunidad();
                self.comprobarSiEsFavorito();
                self.cargarEstadoDelJuego();
                self.cargarSagaDelJuego(nuevoId).then(function() {
                    self.cargarFavoritosDeSaga();
                });
                self.cargarAdiciones(nuevoId);
                self.cargarLogros(nuevoId);
            });
        }
    },

    methods: {

        async cargarDetalleDelJuego(id) {

            try {
                var gameId = id;
                if (!gameId) {
                    gameId = this.$route.params.id;
                }

                this.loading = true;
                this.game = await obtenerDetalleDeJuego(gameId);

            } catch (error) {
                console.error('Error al cargar el detalle del juego:', error);
                this.game = null;
                this.errorMessage = 'Could not load game details. Please try again later.';

            } finally {
                this.loading = false;
            }
        },

        mediaAnterior() {

            var total = this.game.screenshots.length;
            if (this.game.movies != null) {
                total = total + this.game.movies.length;
            }

            this.activeShot = (this.activeShot - 1 + total) % total;
        },

        mediaSiguiente() {

            var total = this.game.screenshots.length;
            if (this.game.movies != null) {
                total = total + this.game.movies.length;
            }

            this.activeShot = (this.activeShot + 1) % total;
        },

        async cargarComentarios() {

            try {
                var gameId = this.$route.params.id;
                var data = await obtenerComentariosDelJuego(gameId, 10, 0);
                this.comments = data.comments;
                this.totalComments = data.total;
                this.hasMoreComments = data.has_more;
                this.sincronizarCalificacionDeMisComentarios();

            } catch (error) {
                console.error('Error al cargar comentarios:', error);
                this.comments = [];
                this.totalComments = 0;
                this.hasMoreComments = false;
            }
        },

        async cargarMasComentarios() {

            if (this.loadingMore || !this.hasMoreComments) {
                return;
            }

            try {
                this.loadingMore = true;
                var gameId = this.$route.params.id;
                var data = await obtenerComentariosDelJuego(gameId, 5, this.comments.length);

                for (var i = 0; i < data.comments.length; i++) {
                    this.comments.push(data.comments[i]);
                }
                this.hasMoreComments = data.has_more;

            } catch (error) {
                console.error('Error al cargar mas comentarios:', error);

            } finally {
                this.loadingMore = false;
            }
        },

        async cargarPromedioDeComunidad() {

            try {
                var gameId = this.$route.params.id;
                var data = await obtenerPromedioDeCalificacion(gameId);

                if (data && data.avg_rating !== undefined && data.avg_rating !== null) {
                    this.communityAvg = data.avg_rating;
                } else {
                    this.communityAvg = 0;
                }

            } catch (error) {
                console.error('Error al cargar la media de la comunidad:', error);
                this.communityAvg = 0;
            }
        },

        // Si el usuario ya comento ponemos su nota en el form para que la
        // vea, pero no lo hacemos si esta editando para no pisarle el valor
        sincronizarCalificacionDeMisComentarios() {

            if (!this.data_user || this.editingId) {
                return;
            }

            for (var i = 0; i < this.comments.length; i++) {
                var c = this.comments[i];
                if (c.id_user === this.data_user.id_user && c.rating) {
                    this.formRating = c.rating;
                    return;
                }
            }
        },

        establecerCalificacionFormulario(valor) {
            this.formRating = valor;
        },

        async publicarComentario() {

            if (!this.newComment || !this.newComment.trim()) {
                notificaciones.warning("Comment cannot be empty.", {
                    title: "Comment required"
                });
                return;
            }

            if (this.newComment.length > 255) {
                notificaciones.warning("Comment cannot exceed 255 characters.", {
                    title: "Comment too long"
                });
                return;
            }

            if (!this.formRating) {
                notificaciones.warning("Select a rating before publishing.", {
                    title: "Rating required"
                });
                return;
            }

            if (this.formRating < 0 || this.formRating > 5) {
                notificaciones.warning("Rating must be between 0 and 5.", {
                    title: "Invalid rating"
                });
                return;
            }

            try {
                var gameId = this.$route.params.id;
                await crearComentario(gameId, this.newComment, this.formRating);

                this.newComment = '';
                this.formRating = 0;
                this.formHover = 0;

                await this.cargarComentarios();
                await this.cargarPromedioDeComunidad();

                notificaciones.success("Your comment was published.", { title: "Comment posted" });

            } catch (error) {
                console.error('Error al agregar comentario:', error);

                var mensajeError = "We couldn't publish your comment. Please try again.";
                if (error.response && error.response.data && error.response.data.message) {
                    mensajeError = error.response.data.message;
                }

                notificaciones.error(mensajeError, {
                    title: "Error posting comment"
                });
            }
        },

        iniciarEdicionComentario(comment) {
            this.editingId = comment.id_comment;
            this.newComment = comment.description;
            if (comment.rating) {
                this.formRating = comment.rating;
            }
        },

        cancelarEdicionComentario() {
            this.editingId = null;
            this.newComment = '';
            this.formHover = 0;
            this.sincronizarCalificacionDeMisComentarios();
        },

        async actualizarMiComentario() {

            if (!this.newComment || !this.newComment.trim()) {
                notificaciones.warning("Comment cannot be empty.", {
                    title: "Comment required"
                });
                return;
            }

            if (this.newComment.length > 255) {
                notificaciones.warning("Comment cannot exceed 255 characters.", {
                    title: "Comment too long"
                });
                return;
            }

            if (!this.formRating) {
                notificaciones.warning("Select a rating before updating.", {
                    title: "Rating required"
                });
                return;
            }

            if (this.formRating < 0 || this.formRating > 5) {
                notificaciones.warning("Rating must be between 0 and 5.", {
                    title: "Invalid rating"
                });
                return;
            }

            try {
                var gameId = this.$route.params.id;
                await actualizarComentario(this.editingId, this.newComment, this.formRating);

                this.editingId = null;
                this.newComment = '';
                this.formRating = 0;
                this.formHover = 0;

                await this.cargarComentarios();
                await this.cargarPromedioDeComunidad();

                notificaciones.success("Comment updated successfully.", { title: "Changes saved" });

            } catch (error) {
                console.log("Error al actualizar el comentario");

                var mensajeError = "We couldn't update your comment.";
                if (error.response && error.response.data && error.response.data.message) {
                    mensajeError = error.response.data.message;
                }

                notificaciones.error(mensajeError, {
                    title: "Error editing comment"
                });
            }
        },

        // Al borrar el comentario tambien quitamos la calificacion para
        // que no quede una nota suelta sin texto asociado
        async eliminarMiComentario(id_comment) {

            try {
                await eliminarComentario(id_comment);

                this.formRating = 0;
                this.formHover = 0;

                var nuevaLista = [];
                for (var i = 0; i < this.comments.length; i++) {
                    if (this.comments[i].id_comment !== id_comment) {
                        nuevaLista.push(this.comments[i]);
                    }
                }
                this.comments = nuevaLista;

                await this.cargarComentarios();
                await this.cargarPromedioDeComunidad();

                notificaciones.success("Your comment and rating were deleted.", { title: "Comment deleted" });

            } catch (error) {
                console.error("Error al eliminar el comentario:", error);
                notificaciones.error("We couldn't delete the comment.", {
                    title: "Error deleting"
                });
            }
        },

        volver() {
            this.$router.push('/content/overview');
        },

        async cargarEstadoDelJuego() {

            if (!estadoAutenticacion.usuario || !this.game || !this.game.id) {
                this.gameStatus = null;
                return;
            }

            try {
                var data = await obtenerEstadoDeJuego(this.game.id);

                if (data && data.status && data.status.status) {
                    this.gameStatus = data.status.status;
                } else {
                    this.gameStatus = null;
                }

            } catch (error) {
                this.gameStatus = null;
            }
        },

        manejarActualizacionEstado(datos) {
            this.gameStatus = datos.status;
        },

        async comprobarSiEsFavorito() {

            if (!estadoAutenticacion.usuario || !this.game || !this.game.id) {
                this.isFavorite = false;
                return;
            }

            try {
                var data = await consultarSiEsFavorito(this.game.id);
                if (data && data.is_favorite) {
                    this.isFavorite = true;
                } else {
                    this.isFavorite = false;
                }

            } catch (error) {
                console.error('Error verificando favorito:', error);
                this.isFavorite = false;
            }
        },

        async alternarFavorito() {

            if (!estadoAutenticacion.usuario) {
                notificaciones.info("Sign in to add games to favorites.", {
                    title: "Sign in required"
                });
                return;
            }

            if (this.favoriteLoading || !this.game || !this.game.id) {
                return;
            }

            this.favoriteLoading = true;

            try {
                if (this.isFavorite) {
                    await quitarDeFavoritos(this.game.id);
                    this.isFavorite = false;
                    this.gameStatus = null;
                    this.showStatusModal = false;
                    notificaciones.success("Game removed from favorites.", { title: "Favorite removed" });
                } else {
                    await agregarAFavoritos(this.game.id);
                    this.isFavorite = true;
                    notificaciones.success("Game added to favorites.", { title: "Favorite added" });
                }

            } catch (error) {
                console.error('Error al cambiar favorito:', error);
                notificaciones.error("We couldn't update your favorites.", {
                    title: "Error"
                });

            } finally {
                this.favoriteLoading = false;
            }
        },

        formatearFecha(valor) {

            if (!valor) {
                return 'Not available';
            }

            var meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            var fecha = new Date(valor);

            return fecha.getDate() + ' ' + meses[fecha.getMonth()] + ' ' + fecha.getFullYear();
        },

        async cargarAdiciones(id) {
            try {
                var gameId = id;
                if (!gameId) {
                    gameId = this.$route.params.id;
                }
                this.adiciones = await obtenerAdiccionesJuego(gameId);
            } catch (error) {
                this.adiciones = [];
            }
        },

        async cargarLogros(id) {
            try {
                var gameId = id;
                if (!gameId) {
                    gameId = this.$route.params.id;
                }
                this.logros = await obtenerLogrosJuego(gameId);
            } catch (error) {
                this.logros = [];
            }
        },

        async cargarSagaDelJuego(id) {
            try {
                var gameId = id;
                if (!gameId) {
                    gameId = this.$route.params.id;
                }
                this.juegosSaga = await obtenerSagaDelJuego(gameId);
            } catch (error) {
                this.juegosSaga = [];
            }
        },

        async cargarFavoritosDeSaga() {
            if (!estadoAutenticacion.usuario || !this.juegosSaga.length) {
                return;
            }
            var nuevoSet = new Set();
            var tareas = this.juegosSaga.map(function(juego) {
                return consultarSiEsFavorito(juego.id).then(function(data) {
                    if (data && data.is_favorite) {
                        nuevoSet.add(juego.id);
                    }
                }).catch(function() {});
            });
            await Promise.all(tareas);
            this.sagaFavoritos = nuevoSet;
        },

        async alternarFavoritoSaga(gameId) {
            if (!estadoAutenticacion.usuario) {
                notificaciones.info("Sign in to add games to favorites.", { title: "Sign in required" });
                return;
            }

            var eraFavorito = this.sagaFavoritos.has(gameId);
            try {
                if (eraFavorito) {
                    await quitarDeFavoritos(gameId);
                    this.sagaFavoritos.delete(gameId);
                    notificaciones.success("Game removed from favorites.", { title: "Favorite removed" });
                } else {
                    await agregarAFavoritos(gameId);
                    this.sagaFavoritos.add(gameId);
                    notificaciones.success("Game added to favorites.", { title: "Favorite added" });
                }
            } catch (error) {
                var mensaje = "We couldn't add the game to favorites.";
                if (eraFavorito) {
                    mensaje = "We couldn't remove the game from favorites.";
                }
                notificaciones.error(mensaje, { title: "Favorites error" });
            }
        },

        irAlJuego(gameId) {
            this.$router.push('/game/' + gameId);
        },

        logroRareza(percent) {
            if (percent === null || percent === undefined) {
                return 'rareza-comun';
            }
            if (percent < 10) {
                return 'rareza-raro';
            }
            if (percent < 40) {
                return 'rareza-infrecuente';
            }
            return 'rareza-comun';
        },

        claseMetacritic(score) {
            if (!score && score !== 0) {
                return 'mc-na';
            }
            if (score >= 80) {
                return 'mc-green';
            }
            if (score >= 50) {
                return 'mc-yellow';
            }
            return 'mc-red';
        },

        // Antes de abrir un enlace externo mostramos un modal para que el
        // usuario sepa que va a salir de la app a un sitio que no controlamos
        abrirEnlaceExterno(url, storeName) {
            this.externalLink.url = url;
            this.externalLink.storeName = storeName;
            this.externalLink.open = true;
        },

        confirmarEnlaceExterno() {
            window.open(this.externalLink.url, '_blank', 'noopener,noreferrer');
            this.externalLink.open = false;
        },

        cancelarEnlaceExterno() {
            this.externalLink.open = false;
        },

        obtenerIconoDeTienda(slug) {

            var iconos = {
                'steam': 'pi-globe',
                'playstation-store': 'pi-mobile',
                'xbox-store': 'pi-microsoft',
                'xbox360': 'pi-microsoft',
                'epic-games': 'pi-bolt',
                'gog': 'pi-star',
                'apple-appstore': 'pi-apple',
                'google-play': 'pi-android',
                'itch': 'pi-heart',
                'nintendo': 'pi-desktop',
                'humble-store': 'pi-gift'
            };

            if (iconos[slug]) {
                return iconos[slug];
            }
            return 'pi-shopping-cart';
        }
    }
};
