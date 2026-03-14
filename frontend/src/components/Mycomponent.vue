<script setup>
import vueLogo from '../assets/vue.svg'
</script>
<style>
    *{
        font-family: 'Arial', sans-serif;

    }
    .header {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    button{
        padding: 2rem;
        border-radius: 10px;
        border: none;
        width: 35%;
        display: block;
        margin: 0 auto;
        cursor: pointer;
        font-size: 1.2rem;
    }
    button:hover{
        background-color: #42b983;
        color: white;
    }

    input{
        display: block;
        margin: 0 auto;
        padding: 1rem;
        width: 50%;
        border-radius: 10px;
        border: 1px solid #ccc;
        font-size: 1.2rem;
        margin-bottom: 13px;
    }

    .highlighted{
        color: #42b983;
    }
</style>
<template>
    
    <div class="header">
        <img :src="vueLogo" class="framework2" alt="Vue logo"  width="100px" height="70px"/>
        <h1>Mi Primer Componente Vue.js</h1>
        <h1 v-bind:class="{highlighted: isHighlighted}">{{ title }}</h1>
    </div>
    <h1 v-if="isVisible">{{ message }}</h1>
    <input type="text" v-model="message">

    <ol>
        <li v-for="name in list" :key="name.id">{{ name.name }}</li>
    </ol>

    <button v-on:click="seyHello()">Boton Visible</button>
    <button v-on:click="toggleHighlight()">Boton Highlight</button>
</template>

<script>
export default {
    name: "Mycomponent",
    data(){
        return {
            message:"Hola, este es mi primer componente Vue.js",
            isVisible: true,
            title:"Game-Rank",
            isHighlighted:false, 

            list: [
                {id: 1, name: "Alan"},
                {id: 2, name: "Mallelin"},
                {id: 3, name: "Franceli"},
                {id: 4, name: "Juan"}
            ]
        }
    },
    methods:{
        toggleVisibilidad(){
            this.isVisible = !this.isVisible;
        },
        seyHello(){
            alert("Hola, este es un método en Vue.js");
        },
        toggleHighlight(){
            this.isHighlighted = !this.isHighlighted;
        }

    }
}
</script>