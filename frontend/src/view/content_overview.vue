<template>
   <body>
     <div class="content-overview">
        <div class="content-input">
            <h1>Contenido Principal</h1>
            <label for="game_id">Id del Juego</label>
            <input type="number" id="game_id" name="game_id" v-model="game_id">
            <button class="btn btn-primary" @click="getContent">Obtener Contenido</button>
            <button @click="logout">Cerrar Sesion</button>
        </div>

        <!-- Card del juego -->
        <div class="game-card" v-if="game">
            <img :src="game.imge_url" :alt="game.name">
            <div class="game-info">
                <h2>{{ game.name }}</h2>
                <p><strong>ID:</strong> {{ game.id }}</p>
                <p><strong>Fecha de lanzamiento:</strong> {{ game.release_date }}</p>
                <p><strong>Rating:</strong> {{ game.rating }}</p>
                <ul>
                    <li><strong>Desarrolladores:</strong> {{ game.developers.join(', ') }}</li>
                </ul>
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
            game: null,
            game_id: null
        }
    },
    

    methods: {
        async getContent() {
            try {
                const response = await getContentOverview(this.game_id);
                this.game = response;
                console.log(response);
                

    

            } catch (error) {
                console.error('Error:', error);
            }
        },
        logout(){
            localStorage.clear();
            this.$router.push("/login")
        }
    }
}

</script>

<style scoped>
label{
    font-size: 1.5rem;
    margin-top: 0.5rem;
    color: black;
}
.content-overview{
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 2rem;
    padding: 2rem;
    background-color: #f0f0f0;
    min-height: 100vh;
}
.content-input{
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: center;
}

.game-card {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
    border: 1px solid black;
    border-radius: 10px;
    padding: 1rem;
    max-width: 700px;
}

.game-card img {
    width: 200px;
    height: 150px;
    object-fit: cover;
    border-radius: 8px;
}

.game-info {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

#game_id{
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid black;
    color: black;
    background-color: white;
    margin-bottom: 2rem;
    margin-top: 1rem;
}
.btn-primary{
    padding: 1rem 3rem;
    border-radius: 10px;
    border: 1px solid white;
    color: white;
    background-color: black;
    cursor: pointer;
}

@media (max-width: 600px){
    .content-overview{
        flex-direction: column;
        align-items: center;
    }
}
button{
    padding: 1rem 4rem;
    border-radius: 10px;
    border: 1px solid white;
    color: white;
    background-color: black;
    cursor: pointer;

}
button:hover{
    box-shadow: inset 0 0 3px 1px black;
    background-color: grey;
    
}
</style>