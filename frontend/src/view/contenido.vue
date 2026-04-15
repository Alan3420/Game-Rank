<template>


    <div class="content-overview">
        <div class="header">
            <h1>Contenido Principal</h1>

            <div class="conten_view">
                <div class="buscar_contenido">
                    <div class="google-search">
                        <InputText class="google-input" v-model="game_name" placeholder="Nombre del juego..." />
                        <Button icon="pi pi-search" class="google-btn" @click="getContentCard" />
                    </div>
                </div>
            </div>
        </div>

        <!-- Card del juego -->
        <div class="card_content">
            <div v-for="game in games" :key="game.id" class="game-card" @click="goToDetail(game.id)">
                <div class="card-image">
                    <img :src="game.imge_url" :alt="game.name" class="game-image" />
                    <div class="image-overlay"></div>
                    <div class="rating-badge">
                        <i class="pi pi-star-fill"></i>
                        <span>{{ game.rating }}</span>
                    </div>
                </div>

                <div class="card-content">
                    <h3 class="game-title">{{ game.name }}</h3>

                    <div class="game-info">
                        <div class="info-item">
                            <i class="pi pi-calendar"></i>
                            <span>{{ game.release_date }}</span>
                        </div>
                    </div>

                    <div class="card-footer">
                        <span class="view-detail">Ver detalles</span>
                        <i class="pi pi-arrow-right"></i>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="showLoadMoreButton" class="load-more-container">
            <Button label="Cargar más juegos" @click="loadMore" :loading="loading" class="load-more-btn" />
        </div>

        <div v-if="loading" class="loader">
            <span>Cargando más juegos...</span>
        </div>
    </div>

</template>

<script>
import { getContentOverview } from "../services/resume_cards";
import { getContentByName } from "../services/buscar"
import InputText from "primevue/inputtext"
import Button from "primevue/button"
export default {
    components: {
        InputText, Button
    },
    data() {
        return {
            games: [],
            game_name: null,
            page: 1,
            per_page: 10,
            loading: false,
            hasNext: true,
            maxGames: 200,
            showLoadMoreButton: false,
            apiCallCount: 0
        }
    },
    mounted() {
        this.getContent();
        this.debouncedScroll = this.debounce(this.handleScroll, 500)
        window.addEventListener("scroll", this.debouncedScroll);

    },
    beforeUnmount() {
        window.removeEventListener("scroll", this.debouncedScroll);
    },


    methods: {
        async getContent() {
            if (this.loading || !this.hasNext || this.games.length >= this.maxGames) return;

            this.loading = true;

            try {
                const response = await getContentOverview(this.page, this.game_name);

                this.games = [...this.games, ...response.games];

                this.hasNext = !!response.next;

                this.page++;
                this.apiCallCount++;

                if (this.apiCallCount >= 2) {
                    this.showLoadMoreButton = true;
                    window.removeEventListener("scroll", this.debouncedScroll);
                }

            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;
            }
        },


        async getContentCard() {
            try {
                if (!this.game_name || this.game_name.trim() === '') {
                    alert("Escribe un nombre de juego")
                    return
                }
                const response = await getContentByName(this.game_name)
                alert(`Resultados: ${JSON.stringify(response)}`)
                console.log(response)
            } catch (error) {
                console.error("ERRORS:", error)
            }
        },

        handleScroll() {
            const scrollTop = window.scrollY;
            const windowHeight = window.innerHeight;
            const fullHeight = document.documentElement.scrollHeight;


            if (this.apiCallCount < 2 && scrollTop + windowHeight >= fullHeight - 1000) {
                this.getContent();
            }
        },

        loadMore() {
            this.getContent();
        },

        goToDetail(gameId) {
            this.$router.push(`/game/${gameId}`);
        },

        debounce(fn, delay) {
            let timer = null
            return function (...args) {
                clearTimeout(timer)
                timer = setTimeout(() => fn.apply(this, args), delay)
            }
        }
    }
}

</script>

<style scoped>
label {
    font-size: 1rem;
    margin-top: 0.5rem;
    color: #444;
}

.content-overview {
    width: 100%;
    /* ← ocupa todo el ancho */
    max-width: 100%;
    /* ← sin límite */
    margin: 0;
    padding: 2rem;
    min-height: 100vh;
    background-color: #f5f5f5;
}

.header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.header h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a1a;
    letter-spacing: 0.03em;
}

.google-search {
    display: flex;
    width: 100%;
    max-width: 600px;
    border-radius: 999px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    background: white;
    border: 1px solid #e0e0e0;
    transition: box-shadow 0.2s ease;
}

.google-search:focus-within {
    box-shadow: 0 4px 20px rgba(124, 111, 255, 0.2);
    border-color: #7c6fff;
}

.google-input {
    flex: 1;
    border: none;
    padding: 0.85rem 1.2rem;
    font-size: 1rem;
    color: #1a1a1a;
    background: transparent;
    outline: none;
}

.google-input::placeholder {
    color: #aaa;
}

.google-btn {
    border: none;
    border-radius: 0 999px 999px 0;
    background: #7c6fff;
    color: white;
    padding: 0 1.4rem;
    cursor: pointer;
    transition: background 0.2s ease;
}

.google-btn:hover {
    background: #5a4de0;
}

/* GRID */
.card_content {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    width: 100%;
    padding: 0 1rem;
}

/* CARD */
.game-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    cursor: pointer;
    position: relative;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.8);
}

.game-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(124, 111, 255, 0.15);
    border-color: #7c6fff;
}

/* IMAGEN */
.card-image {
    position: relative;
    width: 100%;
    height: 200px;
    overflow: hidden;
}

.game-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.game-card:hover .game-image {
    transform: scale(1.05);
}

.image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.1) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.game-card:hover .image-overlay {
    opacity: 1;
}

.rating-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: rgba(255, 193, 7, 0.95);
    color: #333;
    padding: 0.5rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.25rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.rating-badge i {
    color: #ff6b35;
}

/* CONTENIDO */
.card-content {
    padding: 1.5rem;
}

.game-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 0.75rem;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.game-info {
    margin-bottom: 1rem;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 0.25rem;
}

.info-item i {
    color: #7c6fff;
    font-size: 0.85rem;
}

/* FOOTER */
.card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 1rem;
    border-top: 1px solid #f0f0f0;
}

.view-detail {
    font-size: 0.9rem;
    font-weight: 600;
    color: #7c6fff;
    transition: color 0.2s ease;
}

.game-card:hover .view-detail {
    color: #5a4de0;
}

.card-footer i {
    color: #7c6fff;
    font-size: 0.9rem;
    transition: transform 0.2s ease;
}

.game-card:hover .card-footer i {
    transform: translateX(4px);
}

/* ANIMACIÓN */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.game-card {
    animation: fadeIn 0.5s ease-out;
}

/* LOADER */
.loader {
    width: 100%;
    text-align: center;
    padding: 2rem;
    font-size: 1rem;
    color: #888;
}

/* Boton Cargar mas... */
.load-more-container {
    width: 100%;
    text-align: center;
    padding: 2rem 0;
}

.load-more-btn {
    background-color: #7c6fff;
    border: none;
    color: white;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.load-more-btn:hover {
    background-color: #6a5acd;
}

.load-more-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .card_content {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1.5rem;
        padding: 0;
    }

    .card-image {
        height: 180px;
    }

    .game-title {
        font-size: 1.1rem;
    }

    .card-content {
        padding: 1.25rem;
    }
}

@media (max-width: 480px) {
    .card_content {
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1rem;
    }

    .card-image {
        height: 160px;
    }

    .game-title {
        font-size: 1rem;
    }

    .card-content {
        padding: 1rem;
    }

    .rating-badge {
        padding: 0.4rem 0.6rem;
        font-size: 0.8rem;
    }
}
</style>