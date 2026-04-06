<template>
   <header>
        <nav>
            <ul class="nav-links">
                <li><a href="/"><img id="logo" src="/src/assets/logo_GR.png" alt="logo_game_rank"></a></li>
                <div class="user_container">
                    <li><a href="/login">Iniciar Sesión</a></li>
                    <li><a href="/register">Registrarse</a></li>
                </div>
            </ul>
        </nav>
    </header>

  <RouterView />

  <footer>
        <p>&copy; 2026 Game Rank. Todos los derechos reservados.</p>
    </footer>
</template>