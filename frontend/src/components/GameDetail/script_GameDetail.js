import { obtenerDetalleDeJuego, obtenerSagaDelJuego, obtenerAdiccionesJuego, obtenerLogrosJuego } from '../../services/gameDetail';
import { obtenerComentariosDelJuego, crearComentario, eliminarComentario, actualizarComentario } from '../../services/comment_services';
import { agregarAFavoritos, quitarDeFavoritos, consultarSiEsFavorito } from '../../services/favorites_area';
import { obtenerEstadoDeJuego } from '../../services/user_game_status';
import { guardarCalificacion, actualizarCalificacion, eliminarCalificacion, obtenerPromedioDeCalificacion } from '../../services/rate_services';
import { estadoAutenticacion } from '../../store/autenticacion';
import { notificaciones } from '../../store/notificaciones';
import { STATUS_META } from '../../utils/statusMeta.js';
import DOMPurify from 'dompurify';

// Pantalla de detalle de un juego concreto. Es la mas grande del proyecto
// porque junta: descripcion, galeria multimedia (capturas + trailers),
// logros, lista de comentarios con su formulario, saga, DLC, sidebar con
// plataformas/estudios/metadatos y los botones de favorito/estado/tiendas.
//
// Toda la carga se hace en cascada en mounted() y se vuelve a disparar
// cuando cambia el parametro :id de la ruta para que al navegar de un
// juego a otro la pantalla se actualice.
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

        // Devuelve el usuario actual del store. Lo exponemos como computed
        // para usarlo dentro del template sin tener que importar el store ahi.
        data_user() {
            return estadoAutenticacion.usuario;
        },

        // Limpia el HTML de la descripcion del juego antes de inyectarlo
        // con v-html, para evitar XSS si el backend devolviera algo malo.
        descripcionSanitizada() {
            var html = '';
            if (this.game && this.game.description) {
                html = this.game.description;
            }
            return DOMPurify.sanitize(html);
        },

        // Comprueba si el usuario actual ya dejo un comentario en este juego.
        // Lo usamos para deshabilitar el formulario y forzar que use "Edit".
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

        // El formulario se deshabilita si el usuario ya comento y NO esta
        // editando. Si esta editando, debe poder escribir.
        formDisabled() {
            if (this.hasOwnComment && !this.editingId) {
                return true;
            }
            return false;
        },

        // Junta videos + capturas en una sola lista para que la galeria
        // pueda iterar sobre ambos tipos como si fueran un solo array.
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

        this.cargarSagaDelJuego();
        this.cargarAdiciones();
        this.cargarLogros();
    },

    watch: {

        // Cuando el usuario navega de /game/1 a /game/2 desde dentro de la
        // misma pantalla, Vue no destruye el componente: hay que recargar
        // todo a mano. Reseteamos primero para no mostrar datos viejos.
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
                self.cargarSagaDelJuego(nuevoId);
                self.cargarAdiciones(nuevoId);
                self.cargarLogros(nuevoId);
            });
        }
    },

    methods: {

        // Pide al backend todos los datos del juego. El id se puede pasar
        // como argumento (lo usa el watcher de la ruta), o si no, se coge
        // de los params de la ruta actual.
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

        // Botones izquierdo/derecho de la galeria. Calculan el total
        // sumando capturas + videos y aplican modulo para que rote en
        // bucle al llegar al final.
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

        // Pide la primera tanda de comentarios (10) y sincroniza la
        // calificacion del formulario con la del comentario propio
        // por si el usuario ya habia votado.
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

        // Boton "Load more": pide otros 5 comentarios mas a partir del
        // ultimo que tenemos en la lista.
        async cargarMasComentarios() {

            if (this.loadingMore || !this.hasMoreComments) {
                return;
            }

            try {
                this.loadingMore = true;
                var gameId = this.$route.params.id;
                var data = await obtenerComentariosDelJuego(gameId, 5, this.comments.length);

                // Concatenamos los nuevos sin perder los antiguos.
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

        // Pide la media de calificacion de la comunidad para este juego.
        // Si falla o no hay datos dejamos 0 y la UI mostrara "—".
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

        // Si el usuario ya comento, ponemos su calificacion previa en el
        // formulario para que pueda verla. Solo aplica cuando NO estamos
        // editando, para no pisar el valor que el usuario esta cambiando.
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

        // Publica un comentario nuevo + su calificacion asociada.
        // Antes de mandar hacemos validaciones de longitud y de rating.
        async publicarComentario() {

            if (!this.newComment || !this.newComment.trim()) {
                notificaciones.error("Comment cannot be empty.", {
                    title: "Comment required"
                });
                return;
            }

            if (this.newComment.length > 255) {
                notificaciones.error("Comment cannot exceed 255 characters.", {
                    title: "Comment too long"
                });
                return;
            }

            if (!this.formRating) {
                notificaciones.error("Select a rating before publishing.", {
                    title: "Rating required"
                });
                return;
            }

            if (this.formRating < 0 || this.formRating > 5) {
                notificaciones.error("Rating must be between 0 and 5.", {
                    title: "Invalid rating"
                });
                return;
            }

            try {
                var gameId = this.$route.params.id;
                // Guardamos primero la calificacion y luego el comentario.
                await guardarCalificacion(gameId, this.formRating);
                await crearComentario(gameId, this.newComment);

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

        // Pone el comentario seleccionado en modo edicion: copia su texto
        // y su rating al formulario para que el usuario los modifique.
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

        // Guarda la edicion del comentario propio + su calificacion.
        async actualizarMiComentario() {

            if (!this.newComment || !this.newComment.trim()) {
                notificaciones.error("Comment cannot be empty.", {
                    title: "Comment required"
                });
                return;
            }

            if (this.newComment.length > 255) {
                notificaciones.error("Comment cannot exceed 255 characters.", {
                    title: "Comment too long"
                });
                return;
            }

            if (!this.formRating) {
                notificaciones.error("Select a rating before updating.", {
                    title: "Rating required"
                });
                return;
            }

            if (this.formRating < 0 || this.formRating > 5) {
                notificaciones.error("Rating must be between 0 and 5.", {
                    title: "Invalid rating"
                });
                return;
            }

            try {
                var gameId = this.$route.params.id;
                await actualizarCalificacion(gameId, this.formRating);
                await actualizarComentario(this.editingId, this.newComment);

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

        // Elimina un comentario y, si es el del propio usuario, tambien
        // borra su calificacion para que no quede una nota suelta.
        async eliminarMiComentario(id_comment) {

            try {
                var gameId = this.$route.params.id;
                await eliminarComentario(id_comment);
                await eliminarCalificacion(gameId);

                this.formRating = 0;
                this.formHover = 0;

                // Actualizamos la lista local sin el comentario borrado.
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

        // Boton "Back" superior: vuelve al catalogo.
        volver() {
            this.$router.push('/content/overview');
        },

        // Pide el estado guardado para este juego (playing, completed, etc.)
        // y lo deja en gameStatus para que el badge se pinte del color
        // que toque.
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

        // El dropdown de estado emite este evento al cambiar. Solo nos
        // interesa el "status" porque ya sabemos a que juego estamos.
        manejarActualizacionEstado(datos) {
            this.gameStatus = datos.status;
        },

        // Pregunta al backend si este juego es favorito del usuario actual.
        // Si no hay sesion o el juego no se cargo, dejamos false directamente.
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

        // Anade o quita este juego de favoritos. Si no hay sesion mostramos
        // notificacion pidiendo iniciar sesion.
        async alternarFavorito() {

            if (!estadoAutenticacion.usuario) {
                notificaciones.error("Sign in to add games to favorites.", {
                    title: "Access required"
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

        // Formatea una fecha ISO al formato "12 Mar 2026".
        // Las abreviaciones de mes van en ingles para mantener la UI uniforme.
        formatearFecha(valor) {

            if (!valor) {
                return 'Not available';
            }

            var meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            var fecha = new Date(valor);

            return fecha.getDate() + ' ' + meses[fecha.getMonth()] + ' ' + fecha.getFullYear();
        },

        // Pide la lista de DLC y expansiones del juego para pintarlas en
        // el sidebar. Si falla dejamos array vacio y la seccion se oculta.
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

        // Pide la lista de logros del juego.
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

        // Pide los demas juegos de la misma saga para pintarlos al final.
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

        // Navega al detalle de otro juego (DLC, saga, etc.).
        irAlJuego(gameId) {
            this.$router.push('/game/' + gameId);
        },

        // Devuelve la clase CSS para pintar la "rareza" del logro segun
        // el porcentaje de jugadores que lo tienen.
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

        // Devuelve la clase CSS del badge de Metacritic segun la nota.
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

        // Cuando el usuario hace click en una tienda externa, mostramos un
        // modal de aviso antes de abrir el enlace. Asi queda claro que va
        // a salir de la app a un sitio que no controlamos.
        abrirEnlaceExterno(url, storeName) {
            this.externalLink.url = url;
            this.externalLink.storeName = storeName;
            this.externalLink.open = true;
        },

        // Confirma el aviso y abre el enlace en una pestana nueva.
        confirmarEnlaceExterno() {
            window.open(this.externalLink.url, '_blank', 'noopener,noreferrer');
            this.externalLink.open = false;
        },

        cancelarEnlaceExterno() {
            this.externalLink.open = false;
        },

        // Mapa de iconos para cada tienda conocida. Si la tienda no esta
        // en el mapa, usamos el icono generico de carrito.
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
