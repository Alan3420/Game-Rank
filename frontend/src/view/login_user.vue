<template>
    <form @submit.prevent="handleLogin">
        <label for="email">Correo Electrónico:</label>
        <input id="email" v-model="email" type="email" required>

        <label for="password">Contraseña:</label>
        <input id="password" v-model="password" type="password" required>

        <button type="submit">Iniciar Sesión</button>
    </form>
</template>

<script>
import { login } from "../services/user_service";

export default {
    data(){
        return {
            email: "",
            password: ""
        }
    },
    methods:{
        async handleLogin() {
            try {
                const response = await login(this.email, this.password)
                console.log("Respuesta:", response)
            } catch (error) {
                console.log("Error:", error)
            }
}
    }
}
</script>