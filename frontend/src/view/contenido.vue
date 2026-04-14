<template>

    <body>
        <div class="content-overview">
            <div class="header">
                <h1>Contenido Principal</h1>

                <div class="conten_view">
                    <div class="buscar-contenido">
                        <div class="google-search">
                            <InputText class="google-input" v-model="game_name" placeholder="Nombre del juego..." />
                            <Button icon="pi pi-search" class="google-btn" @click="getContentCard" />
                        </div>
                    </div>
                </div>
            </div>

            <!-- Card del juego -->
            <div class="card_content">
                <div v-for="game in games" :key="game.id" class="game-card">
                    <div class="game-bg" :style="{ backgroundImage: `url(${game.imge_url})` }">
                        <div class="overlay">
                            <div class="game-content">
                                <h2 class="game-title">
                                    <span>{{ game.name }} &nbsp;&nbsp;&nbsp; {{ game.name }} &nbsp;&nbsp;&nbsp;</span>
                                </h2>

                                <div class="game-meta">
                                    <span class="meta-item">
                                        <i class="pi pi-star"></i>
                                        {{ game.rating }}
                                    </span>

                                    <span class="meta-item">
                                        <i class="pi pi-calendar"></i>
                                        {{ game.release_date }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <button class="logout" @click="logout">Cerrar Sesion</button>

            <div v-if="loading" class="loader">
                <span>Cargando más juegos...</span>
            </div>
        </div>
    </body>
</template>

<script>
import { getContentOverview } from "../services/resume_cards";
import {getContentByName} from "../services/buscar"
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
            maxGames: 200
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


            if (scrollTop + windowHeight >= fullHeight - 1000) {
                this.getContent();
            }
        },

        debounce(fn, delay) {
            let timer = null
            return function (...args) {
                clearTimeout(timer)
                timer = setTimeout(() => fn.apply(this, args), delay)
            }
        },

        logout() {
            localStorage.clear();
            this.$router.push("/login")
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
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    /* ← de 200 a 250 */
    gap: 1.5rem;
    width: 100%;
}

/* CARD */
.game-card {
    width: 100%;
    height: 500px;
    border-radius: 16px;
    overflow: hidden;
    cursor: pointer;
    position: relative;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.game-card:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 28px rgba(124, 111, 255, 0.25);
}

/* IMAGEN FONDO */
.game-bg {
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center;
}

/* OVERLAY */
.overlay {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: flex-end;
    padding: 1rem;
    background: linear-gradient(to top,
            rgba(0, 0, 0, 0.80) 20%,
            rgba(0, 0, 0, 0.2) 60%,
            rgba(0, 0, 0, 0.0) 100%);
    transition: background 0.3s ease;
}

.game-card:hover .overlay {
    background: linear-gradient(to top,
            rgba(0, 0, 0, 0.92) 30%,
            rgba(0, 0, 0, 0.35) 70%);
}

/* CONTENIDO */
.game-content {
    color: #fff;
    width: 100%;
}

.game-title {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.game-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    opacity: 0.9;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

.meta-item i {
    font-size: 0.85rem;
    transition: transform 0.2s ease;
}

.game-card:hover .meta-item i {
    transform: scale(1.15);
}

.game-title {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
    white-space: nowrap;
    overflow: hidden;
}

.game-title span {
    display: inline-block;
}

.game-card:hover .game-title span {
    animation: marquee 4s linear infinite;
}

/* ANIMACIÓN */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes marquee {
    0% {
        transform: translateX(0);
    }

    100% {
        transform: translateX(-50%);
    }
}

.game-card {
    animation: fadeIn 0.4s ease;
}

/* LOADER */
.loader {
    width: 100%;
    text-align: center;
    padding: 2rem;
    font-size: 1rem;
    color: #888;
}

/* LOGOUT */
.logout {
    margin-top: 2rem;
    padding: 0.75rem 2rem;
    border-radius: 10px;
    border: 1px solid #ddd;
    color: #444;
    background-color: white;
    cursor: pointer;
    transition: background 0.2s ease, border-color 0.2s ease;
    font-size: 0.95rem;
}

.logout:hover {
    background-color: #f0f0f0;
    border-color: #bbb;
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .game-card {
        height: 240px;
    }

    .game-title {
        font-size: 0.9rem;
    }

    .game-meta {
        font-size: 0.8rem;
    }
}

@media (max-width: 480px) {
    .card_content {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    }

    .game-card {
        height: 200px;
    }
}
</style>