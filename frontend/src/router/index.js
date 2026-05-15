import {createRouter, createWebHistory} from "vue-router";
import Login from "../components/LoginRegister/login_user.vue";
import Register from "../components/LoginRegister/register_user.vue"
import Home from "../components/Home/home.vue";
import ContentOverview from "../components/Content/contenido.vue";
import GameDetail from "../components/GameDetail/GameDetail.vue";
import perfil_user from "../components/User/perfil_user.vue";
import AdminUsers from "../components/Admin/AdminUsers.vue";
import TerminosCondiciones from "../components/Legal/TerminosCondiciones.vue";

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
        meta:{title:"Game Rank - Gestión de Usuarios"}
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
})

export default router;
