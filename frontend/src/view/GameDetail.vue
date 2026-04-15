<template>
    <div class="game-detail-page">
        <div v-if="loading" class="detail-loader">
            <span>Cargando detalles del juego...</span>
        </div>

        <div v-else-if="game" class="detail-layout">
            <section class="detail-banner" :style="bannerStyle">
                <div class="detail-banner-overlay">
                    <div class="detail-banner-content">
                        <span class="detail-category">Detalle del juego</span>
                        <h1>{{ game.name }}</h1>
                        <div class="detail-stats">
                            <div><i class="pi pi-star-fill"></i> {{ game.rating ?? 'N/A' }}</div>
                            <div><i class="pi pi-calendar"></i> {{ formatDate(game.release_date) }}</div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="detail-body">
                <div class="detail-card detail-description-card">
                    <h2>Descripción</h2>
                    <div class="detail-description" v-html="game.description || '<em>Descripción no disponible.</em>'"></div>
                </div>

                <aside class="detail-aside">
                    <div class="detail-card">
                        <h3>Plataformas</h3>
                        <div class="tag-list">
                            <span v-if="!game.platforms?.length" class="tag empty">Sin información</span>
                            <span v-for="platform in game.platforms" :key="platform.id" class="tag">{{ platform.name }}</span>
                        </div>
                    </div>

                    <div class="detail-card">
                        <h3>Desarrolladores</h3>
                        <div class="dev-list">
                            <div v-if="!game.developers?.length" class="tag empty">Sin información</div>
                            <div v-for="dev in game.developers" :key="dev.id" class="dev-item">
                                <img v-if="dev.image" :src="dev.image" :alt="dev.name" />
                                <span>{{ dev.name }}</span>
                            </div>
                        </div>
                    </div>
                </aside>
            </section>

            <div class="detail-actions">
                <Button label="Volver al listado" icon="pi pi-arrow-left" class="back-btn" @click="goBack" />
            </div>
        </div>

        <div v-else class="detail-error">
            <h2>{{ errorMessage || 'No se pudieron cargar los detalles del juego.' }}</h2>
            <Button label="Volver" icon="pi pi-arrow-left" class="back-btn" @click="goBack" />
        </div>
    </div>
</template>

<script>
import { getGameDetail } from '../services/gameDetail';
import Button from 'primevue/button';

export default {
    name: 'GameDetail',
    components: { Button },
    data() {
        return {
            game: null,
            loading: true,
            bannerOffset: 0,
            errorMessage: ''
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
</script>

<style scoped>
.game-detail-page {
    min-height: 100vh;
    background: #f5f6fb;
    color: #1f1f35;
    padding: 2rem;
    padding-top: 0;
}

.detail-loader,
.detail-error {
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    background: white;
    border-radius: 24px;
    box-shadow: 0 16px 40px rgba(20, 21, 63, 0.08);
    padding: 2rem;
}

.detail-layout {
    display: grid;
    gap: 2rem;
}

.detail-banner {
    min-height: 560px;
    width: calc(100% + 4rem);
    margin: 0 -2rem;
    border-radius: 0;
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    position: relative;
    display: flex;
    align-items: flex-end;
    overflow: hidden;
    will-change: background-position;
    box-shadow: inset 0 0 0 1px rgba(124, 111, 255, 0.1), 0 24px 60px rgba(12, 12, 24, 0.1);
}

.detail-banner-overlay {
    width: 100%;
    padding: 2.5rem;
    background: linear-gradient(180deg, rgba(19, 18, 51, 0.001) 0%, rgba(19, 18, 51, 0.88) 100%);
}

.detail-banner-content {
    max-width: 760px;
    color: white;
}

.detail-category {
    display: inline-flex;
    padding: 0.5rem 1rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.12);
    color: #f9f9ff;
    font-weight: 700;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

.detail-banner-content h1 {
    margin: 0;
    font-size: clamp(2rem, 2.5vw, 3.2rem);
    line-height: 1.02;
}

.detail-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 1.2rem;
    margin-top: 1.4rem;
    color: #dcdcff;
    font-size: 1rem;
}

.detail-stats div {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.detail-stats i {
    color: #ffd369;
}

.detail-body {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.75rem;
}

.detail-card {
    background: white;
    border-radius: 28px;
    padding: 2rem;
    margin-top: 10px;
    box-shadow: 0 24px 56px rgba(20, 21, 63, 0.08);
}

.detail-card h2,
.detail-card h3 {
    margin-top: 0;
    margin-bottom: 1rem;
    font-size: 1.4rem;
}

.detail-description {
    color: #4c4c66;
    line-height: 1.8;
}

.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
}

.tag,
.tag.empty {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 1rem;
    border-radius: 999px;
    background: #eef0ff;
    color: #4b4f72;
    font-size: 0.95rem;
    font-weight: 600;
}

.dev-list {
    display: grid;
    gap: 1rem;
}

.dev-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border-radius: 18px;
    background: #f9f9ff;
}

.dev-item img {
    width: 48px;
    height: 48px;
    border-radius: 16px;
    object-fit: cover;
}

.dev-item span {
    color: #2b2b45;
    font-weight: 600;
}

.detail-actions {
    display: flex;
    justify-content: flex-start;
}

.back-btn {
    border-radius: 999px;
    background: #7c6fff;
    border: none;
    color: #fff;
    padding: 0.95rem 1.4rem;
}

@media (max-width: 960px) {
    .detail-body {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 680px) {
    .game-detail-page {
        padding: 1.25rem;
    }

    .detail-banner {
        min-height: 260px;
    }

    .detail-card {
        padding: 1.4rem;
    }
}
</style>
