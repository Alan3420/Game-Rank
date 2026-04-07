<template>
  <section class="hero">
    <div class="container-hero">
      <h1>Descubre el juego perfecto para ti</h1>
      <p>Explora nuestra base de datos de videojuegos y encuentra el que mejor se adapte a tus preferencias</p>
      <div class="content-view">
        <button class="btn_principal" @click="goToLogin">Explorar juegos</button>
        <button class="btn_secundario">Como funciona</button>
      </div>
    </div>
  </section>

  <section class="registro_user section_container">
    <div class="container-hero">
      <h2>¿Todavía no tienes cuenta?</h2>
      <p>Únete a nuestra comunidad de jugadores y descubre nuevos juegos</p>
      <button class="btn_registro" @click="goToRegister">Crear cuenta</button>

    </div>
  </section>
</template>

<script>
export default {
  methods: {
    goToLogin() {
      const token = localStorage.getItem("token")
      if (token) {
        this.$router.push('/content/overview');
      } else {
        this.$router.push('/login');
      }
    },
    goToRegister(){
      this.$router.push("/register");
    }
  }
}
</script>

<style scoped>
.hero {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  text-align: center;
  height: 30vh;
  background-color: #ffffff;

  width: 95%;
  margin: 0 auto;
  margin-top: 40px;
  border-radius: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
}

.container-hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  line-height: 1.5;
}

.container-hero p {
  color: #555555;
  margin-bottom: 20px;
}

.content-view {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  gap: 20px;
}
.btn_principal, .btn_secundario{
  border: none;
  padding: 10px 35px;
  border-radius: 15px;
  cursor: pointer;
}

.btn_principal {
  background-color: #6366f1;
  color: white;
}

.btn_principal:hover {
  background-color: #4f46e5;
}

.btn_secundario {
  background-color: #d8d8d8;
  color: #333;

}

.btn_secundario:hover {
  background-color: #adaeaf;
}


@media (max-width: 600px) {
  .hero {
    height: auto;
    padding: 20px;
  }


  .content-view {
    flex-direction: column;
    align-items: center;
  }
}

.section_container{
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  text-align: center;
  height: 30vh;
  background-color: #ffffff;

  width: 95%;
  margin: 0 auto;
  margin-top: 20px;
  border-radius: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
}
.btn_registro {
  background-color: #6366f1;
  color: white;
  border: none;
  padding: 10px 35px;
  border-radius: 15px;
  cursor: pointer;

}
.btn_registro:hover {
  background-color: #4f46e5;
}
</style>
