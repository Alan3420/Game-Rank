<template>
    <div class="home-content">
        <h1>Bienvenido a Game Rank</h1>
        <p>Tu plataforma de reseñas de videojuegos</p>
        <button @click="goToLogin">Iniciar Sesión</button>
    </div>
</template>

<script>
export default {
    methods: {
        goToLogin() {
          const token = localStorage.getItem("token")
          if(token){
            this.$router.push('/content');
          }else{
            this.$router.push('/login');
          }
        }
    }
}
</script>

<style scoped>
    
.home-content{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  min-height: 100vh;
}

.home-content h1{
  color: #111827;

}
.home-content p{
  margin-top: 0.5rem;
  color: #6b7280;
}
.home-content button{
  margin-top: 3rem;
  background-color: #6366f1;
  color: #ffffff;
  padding: 1rem 8rem;
  font-size: 1.1rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.25s ease, transform 0.2s ease;
  
}

.home-content button:hover {
  background-color: #4f46e5;
  transform: translateY(-2px);
}
</style>
