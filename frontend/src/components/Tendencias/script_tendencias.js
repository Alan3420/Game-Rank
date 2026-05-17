import { getTendencias } from '../../services/tendencias';

export default {
    data() {
        return {
            tendencias: null,
            loading: true,
            error: null,
            activeTab: 'mas_favoritos',
        };
    },
    computed: {
        secciones() {
            return [
                {
                    key: 'mas_favoritos',
                    titulo: 'Most Favorited',
                    subtitulo: 'Games with the most likes from the community',
                    icono: 'pi-heart-fill',
                    label: 'Favorited',
                },
                {
                    key: 'mejor_valorados',
                    titulo: 'Top Rated',
                    subtitulo: 'The highest rated titles by the community',
                    icono: 'pi-star-fill',
                    label: 'Rated',
                },
                {
                    key: 'mas_comentados',
                    titulo: 'Most Commented',
                    subtitulo: 'Games with the most discussion and reviews',
                    icono: 'pi-comments',
                    label: 'Commented',
                },
                {
                    key: 'mas_coleccion',
                    titulo: 'Most Collected',
                    subtitulo: 'Titles most added to user collections',
                    icono: 'pi-bookmark-fill',
                    label: 'Collection',
                },
            ];
        },
        seccionActiva() {
            return this.secciones.find(s => s.key === this.activeTab) ?? this.secciones[0];
        },
        juegosActivos() {
            return this.tendencias?.[this.activeTab] ?? [];
        },
    },
    async mounted() {
        try {
            this.tendencias = await getTendencias();
        } catch {
            this.error = 'We couldn\'t load the trends. Please try again later.';
        } finally {
            this.loading = false;
        }
    },
    methods: {
        metacriticClass(score) {
            if (!score) return 'mc-na';
            if (score >= 80) return 'mc-green';
            if (score >= 50) return 'mc-yellow';
            return 'mc-red';
        },
        goToGame(id) {
            this.$router.push(`/game/${id}`);
        },
    },
};
