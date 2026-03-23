<template>

    <body>
        <fieldset>
            <legend>Iniciar Sesion</legend>

            <form @submit.prevent="handleLogin">
                <label for="email">Correo Electrónico:</label>
                <input type="email" id="email" v-model="email" placeholder="email">

                <label for="passwd">Contraseña:</label>
                <input type="password" id="passwd" v-model="password" placeholder="password">

                <button type="submit">Login</button>
            </form>
        </fieldset>
    </body>
</template>

<script>
import { login } from "../services/user_service";

export default {
    data() {
        return {
            email: "",
            password: ""

        }
    },
    methods: {
        async handleLogin() {
            try {
                const response = await login(this.email, this.password)
                localStorage.setItem("token", response.token)
                localStorage.setItem("user", JSON.stringify(response.user))
                this.$router.push('/content');
            } catch (error) {
                console.log("Error:", error)
            }
        }
    }
}
</script>


<style scoped>
body {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;

}

fieldset {
    border-radius: 10px;
    background-color: white;
}

form {
    display: flex;
    flex-direction: column;
    padding: 2rem;

}

form input {
    margin: 3px;
    padding: 0.8rem 4rem;
    padding-left: 2px;
    border-radius: 5px;
    background-color: antiquewhite;
    border: none;

}

form button {
    padding: 0.8rem;
    border-radius: 8px;
    border: none;
    cursor: pointer;
}
</style>
