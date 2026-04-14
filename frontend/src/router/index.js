import {createRouter, createWebHistory} from "vue-router";
import Login from "../view/login_user.vue";
import Register from "../view/register_user.vue"
import Home from "../view/home.vue";
import ContentOverview from "../view/contenido.vue";

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
        path: "/content/overview",
        component: ContentOverview,
        meta:{title:"Game Rank - Content Overview"}
    }
];

const router = createRouter({
    history:createWebHistory(),
    routes
})

router.beforeEach((to) => {
    document.title = to.meta.title || 'GameRank'

    const rutasPublicas = ['/login', '/register',"/"]
    const token = localStorage.getItem("token")

    if(!token && !rutasPublicas.includes(to.path)){
        return "/login"
    }
})

export default router;
