import { getGameDetail } from '../../services/gameDetail';
import { getCommentsByGame, createComments, deleteComment, updateComment } from '../../services/comment_services';

export default {
    name: 'GameDetail',
    
    data() {
        return {
            game: null,
            loading: true,
            bannerOffset: 0,
            errorMessage: '',
            comments: [],
            newComment: '',
            editingId: null,
            editDescription: ''
        };
    },
    computed: {
        bannerStyle() {
            const position = `center calc(50% + ${this.bannerOffset}px)`;
            return {
                backgroundImage: this.game?.imge_url ? `linear-gradient(to bottom, rgba(19, 18, 51, 0.2), rgba(19, 18, 51, 0.85)), url(${this.game.imge_url})` : 'none',
                backgroundPosition: position
            };
        }
    },
    async mounted() {
        window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
        await this.loadGameDetail();
        await this.loadComments();
        this.onScroll = this.handleBannerScroll;
        window.addEventListener('scroll', this.onScroll, { passive: true });
    },
    beforeUnmount() {
        window.removeEventListener('scroll', this.onScroll);
    },
    beforeRouteUpdate(to, from, next) {
        window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
        this.loadGameDetail(to.params.id).then(() => next());
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

        async loadComments() {
            try {
                const gameId = this.$route.params.id;
                const data = await getCommentsByGame(gameId);
                this.comments = data.comments;
            } catch (error) {
                console.error('Error al cargar comentarios:', error);
                this.comments = [];
            }
        },

        handleBannerScroll() {
            const banner = this.$el.querySelector('.detail-banner');
            if (!banner) return;
            const rect = banner.getBoundingClientRect();
            this.bannerOffset = Math.round(rect.top * 0.15);
        },

        goBack() {
            this.$router.push('/content/overview');
        },

        formatDate(value) {
            if (!value) return 'No disponible';
            const date = new Date(value);
            return date.toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }
    }
};
