<template>
   <header>
        <nav>
            <ul class="nav-links">
                <li><a href="/"><img id="logo" src="/src/assets/game_rank_logo.png" alt="logo_game_rank"></a></li>
                <div class="user_container">
                    <li><a href="/login">Iniciar Sesión</a></li>
                    <li><a href="/register">Registrarse</a></li>
                </div>
            </ul>
        </nav>
    </header>

  <main>
    <RouterView />
  </main>

  <footer>

        <div class="footer-info">
            <p>&copy; 2026 Game Rank | Game data powered by <a href="https://rawg.io" target="_blank">RAWG</a></p>
        </div>

        <div class="footer-links">
            <a href="">Terminos</a>
            <a href="">Privacidad</a>
            <a href="https://github.com/Alan3420" target="_blank">Contacto</a>
        </div>
    </footer>
</template>