import {createRouter, createWebHistory} from "vue-router";
import Login from "../components/LoginRegister/login_user.vue";
import Register from "../components/LoginRegister/register_user.vue"
import Home from "../components/Home/home.vue";
import ContentOverview from "../components/Content/contenido.vue";
import GameDetail from "../components/GameDetail/GameDetail.vue";
import perfil_user from "../components/User/perfil_user.vue";
import AdminUsers from "../components/Admin/AdminUsers.vue";
import AdminComments from "../components/Admin/AdminComments.vue";
import TerminosCondiciones from "../components/Legal/TerminosCondiciones.vue";
import Tendencias from "../components/Tendencias/Tendencias.vue";
import NotFound from "../components/NotFound/NotFound.vue";
import { estadoAutenticacion } from "../store/autenticacion";

const routes = [
    {
        path: "/",
        component: Home,
        meta:{title:"Game Rank - Home"}

    },
    {
        path: "/login",
        component: Login,
        meta:{title:"Game Rank - Login"}

    },
    {
        path: "/register",
        component: Register,
        meta:{title:"Game Rank - Register"}
    },
    {
        path: "/terminos",
        component: TerminosCondiciones,
        meta:{title:"Game Rank - Términos y Condiciones"}
    },
    {
        path: "/content/overview",
        component: ContentOverview,
        meta:{title:"Game Rank - Principal"}
    },
    {
        path: "/game/:id",
        component: GameDetail,
        meta:{title:"Game Rank - Detalles"}
    },
    {
        path: "/user/profile",
        component: perfil_user,
        meta:{title:"Game Rank - Perfil"}
    },
    {
        path: "/profile",
        component: perfil_user,
        meta:{title:"Game Rank - Perfil"}
    },
    {
        path: "/admin/users",
        component: AdminUsers,
        meta:{title:"Game Rank - Gestión de Usuarios", requiresAdmin: true}
    },
    {
        path: "/admin/comments",
        component: AdminComments,
        meta:{title:"Game Rank - Moderación de Comentarios", requiresAdmin: true}
    },
    {
        path: "/tendencias",
        component: Tendencias,
        meta:{title:"Game Rank - Tendencias"}
    },
    {
        path: "/:pathMatch(.*)*",
        name: "not-found",
        component: NotFound,
        meta:{title:"Game Rank - Página no encontrada"}
    }
];

const router = createRouter({
    history:createWebHistory(),
    routes
})

router.beforeEach((to) => {
    document.title = to.meta.title || 'GameRank'

    const rutasPublicas = ['/login', '/register', '/', '/terminos']
    const token = localStorage.getItem("token")

    if(!token && !rutasPublicas.includes(to.path)){
        return "/login"
    }

    // Si el usuario ya está cargado y no es admin, muestra 404 manteniendo la URL
    if(to.meta.requiresAdmin && estadoAutenticacion.usuario && estadoAutenticacion.usuario.role !== 'admin'){
        return { name: "not-found", params: { pathMatch: to.path.substring(1).split('/') } }
    }
})

export default router;
