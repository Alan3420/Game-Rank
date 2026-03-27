<template>
   <body>
     <div class="content-overview">
        <h1>Contenido Principal</h1>
        <p id="content"></p>
        <button @click="logout">Cerrar Sesion</button>
    </div>
   </body>
</template>

<script>
import { getContentOverview } from "../services/content_service";

export default {
    data() {
        return {
            contentOverview: null,
            user_id: null
        }
    },
    async mounted() {
        try {
            const response = await getContentOverview(this.contentOverview, this.user_id);
            document.getElementById("content").textContent= JSON.stringify(response.message)
            console.log(JSON.stringify(response.message));
            const user = JSON.parse(localStorage.getItem("user"))
            console.log(user.id_user);
            
        } catch (error) {
            console.error('Error fetching content overview:', error);
        }
    },

    methods: {
        logout(){
            localStorage.clear();
            this.$router.push("/login")
        }
    }
}

</script>

<style scoped>
.content-overview{
    min-height: 80vh;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    
}

@media (max-width: 600px){
    .content-overview{
        flex: 1;
    }
}
button{
    padding: 1rem 3rem;
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