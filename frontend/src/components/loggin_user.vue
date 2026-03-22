<template>
    <form @submit.prevent="login">
        <label for="email">Correo Electrónico:</label>
        <input id="email" v-model="email" type="email" required>

        <label for="password">Contraseña:</label>
        <input id="password" v-model="password" type="password" required>

        <button type="submit">Iniciar Sesión</button>
    </form>
</template>

<script>
export default {
    data(){
        return {
            email: "",
            password: ""
        }
    },
    methods:{
        login(){
            console.log("Email:", this.email);

            fetch("http://localhost:5000/user/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password
                })
            })
        }
    }
}
    
</script>