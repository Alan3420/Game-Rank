import { createRouter, createWebHistory } from "vue-router";
import { estadoAutenticacion } from "../store/autenticacion";

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
        path: "/:pathMatch(.*)*",
        name: "not-found",
        component: NotFound,
        meta: { title: "Game Rank - Página no encontrada" }
    }
];


const router = createRouter({
    history: createWebHistory(),
    routes: routes,

    scrollBehavior: function () {
        return { top: 0, behavior: 'smooth' };
    }
});


router.beforeEach(function (to) {

    if (to.meta && to.meta.title) {
        document.title = to.meta.title;
    } else {
        document.title = 'GameRank';
    }

    var rutasPublicas = ['/login', '/register', '/', '/terminos'];
    var token = localStorage.getItem("token");

    if (!token && rutasPublicas.indexOf(to.path) === -1) {
        return "/login";
    }

    if (to.meta && to.meta.requiresAdmin) {
        // Si no es admin sacamos un 404 en vez de un 403 para no
        // delatar que la ruta de admin existe
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
