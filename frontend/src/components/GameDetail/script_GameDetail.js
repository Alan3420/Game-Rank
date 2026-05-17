import { getGameDetail, obtenerSagaDelJuego, obtenerAdiccionesJuego, obtenerLogrosJuego } from '../../services/gameDetail';
import { getCommentsByGame, createComments, deleteComment, updateComment } from '../../services/comment_services';
import { addTOFavorite, removeTOFavorite, checkFavorite } from '../../services/favorites_area';
import { getGameStatus } from '../../services/user_game_status';
import { saveRate, updateRate, deleteRate, getAvgRate } from '../../services/rate_services';
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
            formRating: 0,
            formHover: 0,
            communityAvg: 0,
            gameStatus: null,
            showStatusModal: false,
            STATUS_META,
            juegosSaga: [],
            adiciones: [],
            logros: [],
            externalLink: { open: false, url: '', storeName: '' }
        };
    },
    computed: {
        data_user() {
            return estadoAutenticacion.usuario;
        },

        descripcionSanitizada() {
            return DOMPurify.sanitize(this.game?.description || '');
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
        this.cargarAdiciones();
        this.cargarLogros();
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
            this.adiciones = [];
            this.logros = [];
            this.comments = [];
            this.totalComments = 0;
            this.hasMoreComments = false;
            this.loadGameDetail(newId).then(() => {
                this.loadComments();
                this.loadCommunityAvg();
                this.checkIsFavorite();
                this.loadStatus();
                this.cargarSagaDelJuego(newId);
                this.cargarAdiciones(newId);
                this.cargarLogros(newId);
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
                this.errorMessage = 'Could not load game details. Please try again later.';
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
                const data = await getCommentsByGame(gameId, 10, 0);
                this.comments = data.comments;
                this.totalComments = data.total;
                this.hasMoreComments = data.has_more;
                this.syncFormRatingFromUserComments();
            } catch (error) {
                console.error('Error al cargar comentarios:', error);
                this.comments = [];
                this.totalComments = 0;
                this.hasMoreComments = false;
            }
        },

        async cargarMasComentarios() {
            if (this.loadingMore || !this.hasMoreComments) return;
            try {
                this.loadingMore = true;
                const gameId = this.$route.params.id;
                const data = await getCommentsByGame(gameId, 5, this.comments.length);
                this.comments = [...this.comments, ...data.comments];
                this.hasMoreComments = data.has_more;
            } catch (error) {
                console.error('Error al cargar más comentarios:', error);
            } finally {
                this.loadingMore = false;
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
                const gameId = this.$route.params.id;
                await saveRate(gameId, this.formRating);
                await createComments(gameId, this.newComment);

                this.newComment = '';
                this.formRating = 0;
                this.formHover = 0;
                await this.loadComments();
                await this.loadCommunityAvg();

                notificaciones.success("Your comment was published.", { title: "Comment posted" });

            } catch (error) {
                console.error('Error al agregar comentario:', error);

                let mensajeError = "We couldn't publish your comment. Please try again.";
                if (error.response?.data?.message) {
                    mensajeError = error.response.data.message;
                }

                notificaciones.error(mensajeError, {
                    title: "Error posting comment"
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
                const gameId = this.$route.params.id;
                await updateRate(gameId, this.formRating);
                await updateComment(this.editingId, this.newComment);

                this.editingId = null;
                this.newComment = '';
                this.formRating = 0;
                this.formHover = 0;
                await this.loadComments();
                await this.loadCommunityAvg();
                notificaciones.success("Comment updated successfully.", { title: "Changes saved" });
            }
            catch (error) {
                console.log("Error al actualizar el comentario");

                let mensajeError = "We couldn't update your comment.";
                if (error.response?.data?.message) {
                    mensajeError = error.response.data.message;
                }

                notificaciones.error(mensajeError, {
                    title: "Error editing comment"
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
                notificaciones.success("Your comment and rating were deleted.", { title: "Comment deleted" });
            }
            catch (error) {
                console.error("Error al eliminar el comentario:", error);
                notificaciones.error("We couldn't delete the comment.", {
                    title: "Error deleting"
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
                notificaciones.error("Sign in to add games to favorites.", {
                    title: "Access required"
                });
                return;
            }
            if (this.favoriteLoading || !this.game?.id) return;

            this.favoriteLoading = true;
            try {
                if (this.isFavorite) {
                    await removeTOFavorite(this.game.id);
                    this.isFavorite = false;
                    notificaciones.success("Game removed from favorites.", { title: "Favorite removed" });
                } else {
                    await addTOFavorite(this.game.id);
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

        formatDate(value) {
            if (!value) return 'Not available';
            const date = new Date(value);
            const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
        },

        async cargarAdiciones(id = null) {
            try {
                const gameId = id || this.$route.params.id;
                this.adiciones = await obtenerAdiccionesJuego(gameId);
            } catch {
                this.adiciones = [];
            }
        },

        async cargarLogros(id = null) {
            try {
                const gameId = id || this.$route.params.id;
                this.logros = await obtenerLogrosJuego(gameId);
            } catch {
                this.logros = [];
            }
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

        logroRareza(percent) {
            if (percent === null || percent === undefined) return 'rareza-comun';
            if (percent < 10) return 'rareza-raro';
            if (percent < 40) return 'rareza-infrecuente';
            return 'rareza-comun';
        },

        metacriticClass(score) {
            if (!score && score !== 0) return 'mc-na';
            if (score >= 80) return 'mc-green';
            if (score >= 50) return 'mc-yellow';
            return 'mc-red';
        },

        openExternalLink(url, storeName) {
            this.externalLink.url = url;
            this.externalLink.storeName = storeName;
            this.externalLink.open = true;
        },

        confirmExternalLink() {
            window.open(this.externalLink.url, '_blank', 'noopener,noreferrer');
            this.externalLink.open = false;
        },

        cancelExternalLink() {
            this.externalLink.open = false;
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
