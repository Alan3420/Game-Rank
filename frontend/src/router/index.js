import { createRouter, createWebHistory } from "vue-router";
import { estadoAutenticacion } from "../store/autenticacion";

// Importacion de los componentes asociados a cada ruta de la SPA.
// Se importan de forma directa (sin lazy) porque la app es pequena y asi
// evitamos el flash de carga entre pantallas.
import Login from "../components/LoginRegister/login_user.vue";
import Register from "../components/LoginRegister/register_user.vue";
import Home from "../components/Home/home.vue";
import ContentOverview from "../components/Content/contenido.vue";
import GameDetail from "../components/GameDetail/GameDetail.vue";
import perfil_user from "../components/User/perfil_user.vue";
import AdminUsers from "../components/Admin/AdminUsers.vue";
import AdminComments from "../components/Admin/AdminComments.vue";
import TerminosCondiciones from "../components/Legal/TerminosCondiciones.vue";
import Tendencias from "../components/Tendencias/Tendencias.vue";
import NotFound from "../components/NotFound/NotFound.vue";


// Definicion centralizada de rutas. Cada ruta declara su componente y el
// titulo de pestana que tendra el navegador. Las rutas con requiresAdmin
// solo pueden visitarse si el usuario logueado tiene rol "admin".
const routes = [
    {
        path: "/",
        component: Home,
        meta: { title: "Game Rank - Home" }
    },
    {
        path: "/login",
        component: Login,
        meta: { title: "Game Rank - Login" }
    },
    {
        path: "/register",
        component: Register,
        meta: { title: "Game Rank - Register" }
    },
    {
        path: "/terminos",
        component: TerminosCondiciones,
        meta: { title: "Game Rank - Términos y Condiciones" }
    },
    {
        path: "/content/overview",
        component: ContentOverview,
        meta: { title: "Game Rank - Principal" }
    },
    {
        path: "/game/:id",
        component: GameDetail,
        meta: { title: "Game Rank - Detalles" }
    },
    {
        path: "/user/profile",
        component: perfil_user,
        meta: { title: "Game Rank - Perfil" }
    },
    {
        path: "/profile",
        component: perfil_user,
        meta: { title: "Game Rank - Perfil" }
    },
    {
        path: "/admin/users",
        component: AdminUsers,
        meta: { title: "Game Rank - Gestión de Usuarios", requiresAdmin: true }
    },
    {
        path: "/admin/comments",
        component: AdminComments,
        meta: { title: "Game Rank - Moderación de Comentarios", requiresAdmin: true }
    },
    {
        path: "/tendencias",
        component: Tendencias,
        meta: { title: "Game Rank - Tendencias" }
    },
    {
        // Catch-all: cualquier ruta no declarada arriba cae aqui y se muestra
        // la pagina 404 conservando la URL original.
        path: "/:pathMatch(.*)*",
        name: "not-found",
        component: NotFound,
        meta: { title: "Game Rank - Página no encontrada" }
    }
];


const router = createRouter({
    history: createWebHistory(),
    routes: routes,

    // Por defecto cada cambio de ruta vuelve al inicio de la pagina.
    // Sin esto el navegador conservaria el scroll de la pantalla anterior
    // y se veria raro al abrir el detalle de un juego.
    scrollBehavior: function () {
        return { top: 0, behavior: 'smooth' };
    }
});


// Guardia de navegacion global. Se ejecuta antes de entrar a cualquier ruta.
// Se encarga de:
//   1. Actualizar el titulo de la pestana del navegador.
//   2. Redirigir al login si la ruta requiere sesion y no hay token.
//   3. Mostrar 404 si la ruta es de admin y el usuario actual no lo es.
router.beforeEach(function (to) {

    if (to.meta && to.meta.title) {
        document.title = to.meta.title;
    } else {
        document.title = 'GameRank';
    }

    var rutasPublicas = ['/login', '/register', '/', '/terminos'];
    var token = localStorage.getItem("token");

    // Sin token y ruta privada -> mandamos al login.
    if (!token && rutasPublicas.indexOf(to.path) === -1) {
        return "/login";
    }

    // Si ya cargamos el usuario y la ruta requiere admin, validamos el rol.
    // Si el usuario no es admin devolvemos 404 manteniendo la URL para no
    // revelar que la ruta existe.
    if (to.meta && to.meta.requiresAdmin) {
        if (estadoAutenticacion.usuario && estadoAutenticacion.usuario.role !== 'admin') {
            var partesRuta = to.path.substring(1).split('/');
            return {
                name: "not-found",
                params: { pathMatch: partesRuta }
            };
        }
    }
});


export default router;
