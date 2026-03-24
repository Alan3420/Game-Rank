<template>
   <body>
     <div class="content-overview">
        <h1>Contenido Principal</h1>
        <button @click="logout">Cerrar Sesion</button>
    </div>
   </body>
</template>

<script>
import { getContentOverview } from "../services/content_service";

export default {
    data() {
        return {
            contentOverview: null
        }
    },
    async mounted() {
        try {
            this.contentOverview = await getContentOverview;
        } catch (error) {
            console.error('Error fetching content overview:', error);
        }
    },

    methods: {
        logout(){
            
        }
    }
}

</script>

<style scoped>
.content-overview{
    min-height: 100vh;
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
</style>