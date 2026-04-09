<template>

    <body>
        <div class="content-overview">
            <div class="content-input">
                <h1>Contenido Principal</h1>

                <div class="conten_view">
                    <div class="content-input">
                        <label for="game_id">Id del Juego</label>
                        <input type="number" id="game_id" name="game_id" v-model="game_id">
                        <button class="btn btn-primary" @click="getContent">Obtener Por ID</button>
                    </div>

                    <div class="content-input">
                        <label for="game_name">Nombre del Juego</label>
                        <input type="text" id="game_name" name="game_name" v-model="game_name">
                        <button class="btn-primary" @click="getContentByName">Buscar por Nombre</button>
                    </div>
                </div>

                <button @click="logout">Cerrar Sesion</button>
            </div>

            <!-- Card del juego -->
            <div class="card_content">
                <div v-for="game in games" :key="game.id" class="game-card">
                    <img :src="game.imge_url" :alt="game.name">
                    <div class="game-info">
                        <h2>{{ game.name }}</h2>
                        <p><strong>ID:</strong> {{ game.id }}</p>
                        <p><strong>Fecha de lanzamiento:</strong> {{ game.release_date }}</p>
                        <strong>Plataformas:</strong> 
                        <ul v-for="platform in game.platforms"> 
                            <li >
                                {{ platform.name }}
                            </li>
                        </ul>
                        <p><strong>Rating:</strong> {{ game.rating }}</p>
                        <strong>Descripción:</strong><p v-html="game.description"></p>
                        <strong>Desarrolladores:</strong>
                        <ul v-for="developer in game.developers">
                            
                            <li>
                                {{ developer.name }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </body>
</template>

<script>
import { getContentOverview } from "../services/content_service";

export default {
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
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 2rem;
    padding: 2rem;
    background-color: #f0f0f0;
    min-height: 100vh;
}

.content-input {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: center;
}

.conten_view {
    display: flex;
    flex-direction: row;
    gap: 1rem;
}
.card_content {
    display: flex;
    flex-direction: column;
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
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid black;
    color: black;
    background-color: white;
    margin-bottom: 2rem;
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

button {
    padding: 1rem 3rem;
    border-radius: 10px;
    border: 1px solid white;
    color: white;
    background-color: black;
    cursor: pointer;

}

button:hover {
    box-shadow: inset 0 0 3px 1px black;
    background-color: grey;

}
</style>