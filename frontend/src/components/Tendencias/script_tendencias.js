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
                    titulo: 'Más Favoritos',
                    subtitulo: 'Los juegos con más me gusta de la comunidad',
                    icono: 'pi-heart-fill',
                    label: 'Favoritos',
                },
                {
                    key: 'mejor_valorados',
                    titulo: 'Mejor Valorados',
                    subtitulo: 'Los títulos mejor puntuados por la comunidad',
                    icono: 'pi-star-fill',
                    label: 'Valorados',
                },
                {
                    key: 'mas_comentados',
                    titulo: 'Más Comentados',
                    subtitulo: 'Los juegos con más debate y reseñas',
                    icono: 'pi-comments',
                    label: 'Comentados',
                },
                {
                    key: 'mas_coleccion',
                    titulo: 'Más en Colección',
                    subtitulo: 'Los títulos más añadidos a colecciones de usuarios',
                    icono: 'pi-bookmark-fill',
                    label: 'Colección',
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
            this.error = 'No se pudieron cargar las tendencias. Inténtalo de nuevo más tarde.';
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
