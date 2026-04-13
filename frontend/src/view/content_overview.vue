<template>

    <body>
        <div class="content-overview">
            <div class="header">
                <h1>Contenido Principal</h1>

                <div class="conten_view">
                    <div class="buscar-contenido">
                        <div class="google-search">
                            <InputText class="google-input" v-model="game_name" placeholder="Nombre del juego..." />
                            <Button icon="pi pi-search" class="google-btn" @click="getContentByName" />
                        </div>
                    </div>
                </div>
            </div>

            <!-- Card del juego -->
            <div class="card_content">
                <div v-for="game in games" :key="game.id" class="game-card">
                    <img :src="game.imge_url" :alt="game.name">
                    <div class="game-info">
                        <h2>{{ game.name }}</h2>
                        <p><strong>Fecha de lanzamiento:</strong> {{ game.release_date }}</p>
                        <p><strong>Rating:</strong> {{ game.rating }}</p>

                    </div>
                </div>
            </div>

            <button class="logout" @click="logout">Cerrar Sesion</button>
        </div>
    </body>
</template>

<script>
import { getContentOverview } from "../services/content_service";
import InputText from "primevue/inputtext"
import Button from "primevue/button"
export default {
    components: {
        InputText, Button
    },
    data() {
        return {
            contentOverview: null,
            games: [],
            game_id: null,
            game_name: null
        }
    },


    methods: {
        async getContent() {
            try {
                const response = await getContentOverview(this.game_id, null);
                this.games = Array.isArray(response) ? response : [response];
                console.log(response);




            } catch (error) {
                console.error('Error:', error);
            }
        },
        async getContentByName() {
            try {
                const response = await getContentOverview(null, this.game_name);
                this.games = Array.isArray(response) ? response : [response];
                console.log(response);


            } catch (error) {
                console.error('Error:', error);
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
    font-size: 1.5rem;
    margin-top: 0.5rem;
    color: black;
}

.content-overview {
    justify-content: center;
    align-items: flex-start;
    gap: 2rem;
    padding: 2rem;
    background-color: #f0f0f0;
    min-height: 100vh;
}

.header {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.buscar-contenido {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    width: 100%;
    align-items: center;
}

.google-search {
    display: flex;
    width: 100%;
    max-width: 650px;
    margin: 0 auto 2rem;
    border-radius: 999px;
    overflow: hidden;
    box-shadow: 0 4px 18px rgba(0,0,0,0.1);
    background: white;
}

.google-input {
    flex: 1;
    border: none;
    padding: 1rem 1.2rem;
}

.google-btn {
    border: none;
    border-radius: 0;
    margin-right: 15px;
}

.conten_view {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.card_content {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
    gap: 1rem;
}

.game-card {
    display: flex;
    gap: 1rem;
    border: 1px solid black;
    border-radius: 10px;
    padding: 1rem;
    width: 700px;
    height: 260px;
}

.game-card img {
    width: 200px;
    height: 100%;
    object-fit: cover;
    border-radius: 8px;
}

.game-info {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    overflow-y: auto;

}

#game_id {
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid black;
    color: black;
    background-color: white;
    margin-bottom: 2rem;
    margin-top: 1rem;
}

#game_name {
    flex: 1;

    margin-top: 1rem;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid black;
    color: black;
    background-color: white;
    margin: 0;
}

.btn-primary {
    padding: 1rem 3rem;
    border-radius: 10px;
    border: 1px solid white;
    color: white;
    background-color: black;
    cursor: pointer;
}

@media (max-width: 600px) {
    .content-overview {
        flex-direction: column;
        align-items: center;
    }
}

.logout {
    padding: 1rem 3rem;
    border-radius: 10px;
    border: 1px solid white;
    color: white;
    background-color: black;
    cursor: pointer;

}

.logout:hover {
    box-shadow: inset 0 0 3px 1px black;
    background-color: grey;

}
</style>