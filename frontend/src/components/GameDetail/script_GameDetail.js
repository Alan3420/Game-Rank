import { getGameDetail, obtenerSagaDelJuego } from '../../services/gameDetail';
import { getCommentsByGame, createComments, deleteComment, updateComment } from '../../services/comment_services';
import { addTOFavorite, removeTOFavorite, checkFavorite } from '../../services/favorites_area';
import { getGameStatus } from '../../services/user_game_status';
import { saveRate, updateRate, deleteRate, getAvgRate } from '../../services/rate_services';
import { estadoAutenticacion } from '../../store/autenticacion';
import { notificaciones } from '../../store/notificaciones';
import { STATUS_META } from '../../utils/statusMeta.js';

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
            STATUS_META,
            juegosSaga: []
        };
    },
    computed: {
        data_user() {
            return estadoAutenticacion.usuario;
        },

        hasOwnComment() {
            if (!this.data_user) return false;
            return this.comments.some(c => c.id_user === this.data_user.id_user);
        },

        formDisabled() {
            return this.hasOwnComment && !this.editingId;
        },

        mediaItems() {
            const videos = (this.game?.movies || []).map(m => ({
                type: 'video',
                url: m.trailer_url,
                name: m.name,
                preview: m.preview
            }));

            const images = (this.game?.screenshots || []).map(s => ({
                type: 'image',
                url: s.image
            }));
            return [...videos, ...images];
        },
    },

    async mounted() {
        window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
        await this.loadGameDetail();
        await this.loadComments();
        await this.loadCommunityAvg();
        await this.checkIsFavorite();
        await this.loadStatus();
        this.cargarSagaDelJuego();
    },

    watch: {
        '$route.params.id'(newId, oldId) {
            if (!newId || newId === oldId) return;
            window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
            this.formRating = 0;
            this.formHover = 0;
            this.editingId = null;
            this.newComment = '';
            this.gameStatus = null;
            this.showStatusModal = false;
            this.juegosSaga = [];
            this.loadGameDetail(newId).then(() => {
                this.loadComments();
                this.loadCommunityAvg();
                this.checkIsFavorite();
                this.loadStatus();
                this.cargarSagaDelJuego(newId);
            });
        }
    },

    methods: {
        async loadGameDetail(id = null) {
            try {
                const gameId = id || this.$route.params.id;
                this.loading = true;
                this.game = await getGameDetail(gameId);
            } catch (error) {
                console.error('Error al cargar el detalle del juego:', error);
                this.game = null;
                this.errorMessage = 'No se pudo cargar el detalle del juego. Inténtalo de nuevo más tarde.';
            } finally {
                this.loading = false;
            }
        },

        prevShot() {

            let total_pct = this.game.screenshots.length
            if (this.game.movies != null) {
                total_pct += this.game.movies.length
            }

            this.activeShot = (this.activeShot - 1 + total_pct) % total_pct;
        },
        nextShot() {

            let total_pct = this.game.screenshots.length
            if (this.game.movies != null) {
                total_pct += this.game.movies.length
            }

            this.activeShot = (this.activeShot + 1) % total_pct;
        },

        async loadComments() {
            try {
                const gameId = this.$route.params.id;
                const data = await getCommentsByGame(gameId);
                this.comments = data.comments;
                this.syncFormRatingFromUserComments();
            } catch (error) {
                console.error('Error al cargar comentarios:', error);
                this.comments = [];
            }
        },

        async loadCommunityAvg() {
            try {
                const gameId = this.$route.params.id;
                const data = await getAvgRate(gameId);
                this.communityAvg = data?.avg_rating ?? 0;
            } catch (error) {
                console.error('Error al cargar la media de la comunidad:', error);
                this.communityAvg = 0;
            }
        },

        syncFormRatingFromUserComments() {
            if (!this.data_user || this.editingId) return;
            const mine = this.comments.find(c => c.id_user === this.data_user.id_user && c.rating);
            if (mine) this.formRating = mine.rating;
        },

        setFormRating(value) {
            this.formRating = value;
        },

        async addComment() {
            if (!this.newComment?.trim()) {
                notificaciones.error("El comentario no puede estar vacío.", {
                    title: "Comentario requerido"
                });
                return;
            }

            if (this.newComment.length > 255) {
                notificaciones.error("El comentario no puede exceder 255 caracteres.", {
                    title: "Comentario muy largo"
                });
                return;
            }

            if (!this.formRating) {
                notificaciones.error("Selecciona una valoración antes de publicar.", {
                    title: "Valoración requerida"
                });
                return;
            }

            if (this.formRating < 0 || this.formRating > 5) {
                notificaciones.error("La valoración debe estar entre 0 y 5.", {
                    title: "Valoración inválida"
                });
                return;
            }

            try {
                const gameId = this.$route.params.id;
                await saveRate(gameId, this.formRating);
                await createComments(gameId, this.newComment);

                this.newComment = '';
                this.formRating = 0;
                this.formHover = 0;
                await this.loadComments();
                await this.loadCommunityAvg();

                notificaciones.success("Tu comentario fue publicado.", { title: "Comentario enviado" });

            } catch (error) {
                console.error('Error al agregar comentario:', error);

                let mensajeError = "No pudimos publicar tu comentario. Inténtalo de nuevo.";
                if (error.response?.data?.message) {
                    mensajeError = error.response.data.message;
                }

                notificaciones.error(mensajeError, {
                    title: "Error al comentar"
                });
            }
        },

        editar(comment) {
            this.editingId = comment.id_comment;
            this.newComment = comment.description;
            if (comment.rating) this.formRating = comment.rating;
        },
        cancelarEdit() {
            this.editingId = null;
            this.newComment = '';
            this.formHover = 0;
            this.syncFormRatingFromUserComments();
        },
        async updComment() {
            if (!this.newComment?.trim()) {
                notificaciones.error("El comentario no puede estar vacío.", {
                    title: "Comentario requerido"
                });
                return;
            }

            if (this.newComment.length > 255) {
                notificaciones.error("El comentario no puede exceder 255 caracteres.", {
                    title: "Comentario muy largo"
                });
                return;
            }

            if (!this.formRating) {
                notificaciones.error("Selecciona una valoración antes de actualizar.", {
                    title: "Valoración requerida"
                });
                return;
            }

            if (this.formRating < 0 || this.formRating > 5) {
                notificaciones.error("La valoración debe estar entre 0 y 5.", {
                    title: "Valoración inválida"
                });
                return;
            }

            try {
                const gameId = this.$route.params.id;
                await updateRate(gameId, this.formRating);
                await updateComment(this.editingId, this.newComment);

                this.editingId = null;
                this.newComment = '';
                this.formRating = 0;
                this.formHover = 0;
                await this.loadComments();
                await this.loadCommunityAvg();
                notificaciones.success("Comentario actualizado correctamente.", { title: "Cambios guardados" });
            }
            catch (error) {
                console.log("Error al actualizar el comentario");

                let mensajeError = "No pudimos actualizar tu comentario.";
                if (error.response?.data?.message) {
                    mensajeError = error.response.data.message;
                }

                notificaciones.error(mensajeError, {
                    title: "Error al editar"
                });
            }
        },
        async delComment(id_comment) {
            try {
                const gameId = this.$route.params.id;
                await deleteComment(id_comment);
                await deleteRate(gameId);
                this.formRating = 0;
                this.formHover = 0;
                this.comments = this.comments.filter(comment => comment.id_comment !== id_comment);
                await this.loadComments();
                await this.loadCommunityAvg();
                notificaciones.success("Tu comentario y valoración fueron eliminados.", { title: "Comentario eliminado" });
            }
            catch (error) {
                console.error("Error al eliminar el comentario:", error);
                notificaciones.error("No pudimos eliminar el comentario.", {
                    title: "Error al eliminar"
                });
            }
        },

        goBack() {
            this.$router.push('/content/overview');
        },

        async loadStatus() {
            if (!estadoAutenticacion.usuario || !this.game?.id) {
                this.gameStatus = null;
                return;
            }
            try {
                const data = await getGameStatus(this.game.id);
                this.gameStatus = data?.status?.status || null;
            } catch {
                this.gameStatus = null;
            }
        },

        handleStatusUpdate({ status }) {
            this.gameStatus = status;
        },

        async checkIsFavorite() {
            if (!estadoAutenticacion.usuario || !this.game?.id) {
                this.isFavorite = false;
                return;
            }
            try {
                const data = await checkFavorite(this.game.id);
                this.isFavorite = !!data?.is_favorite;
            } catch (error) {
                console.error('Error verificando favorito:', error);
                this.isFavorite = false;
            }
        },

        async toggleFavorite() {
            if (!estadoAutenticacion.usuario) {
                notificaciones.error("Inicia sesión para añadir juegos a favoritos.", {
                    title: "Acceso requerido"
                });
                return;
            }
            if (this.favoriteLoading || !this.game?.id) return;

            this.favoriteLoading = true;
            try {
                if (this.isFavorite) {
                    await removeTOFavorite(this.game.id);
                    this.isFavorite = false;
                    notificaciones.success("Juego eliminado de favoritos.", { title: "Favorito eliminado" });
                } else {
                    await addTOFavorite(this.game.id);
                    this.isFavorite = true;
                    notificaciones.success("Juego añadido a favoritos.", { title: "Favorito añadido" });
                }
            } catch (error) {
                console.error('Error al cambiar favorito:', error);
                notificaciones.error("No pudimos actualizar tus favoritos.", {
                    title: "Error"
                });
            } finally {
                this.favoriteLoading = false;
            }
        },

        formatDate(value) {
            if (!value) return 'No disponible';
            const date = new Date(value);
            const meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
            return `${date.getDate()} ${meses[date.getMonth()]} ${date.getFullYear()}`;
        },

        async cargarSagaDelJuego(id = null) {
            try {
                const gameId = id || this.$route.params.id;
                this.juegosSaga = await obtenerSagaDelJuego(gameId);
            } catch {
                this.juegosSaga = [];
            }
        },

        irAlJuego(gameId) {
            this.$router.push(`/game/${gameId}`);
        },

        getStoreIcon(slug) {
            const icons = {
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
                'humble-store': 'pi-gift',
            };
            return icons[slug] ?? 'pi-shopping-cart';
        }
    }
};
