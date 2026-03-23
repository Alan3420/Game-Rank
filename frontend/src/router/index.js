import {createRouter, createWebHistory} from "vue-router";
import Login from "../view/login_user.vue";
import Home from "../view/home.vue";
import ContentOverview from "../view/content_overview.vue";

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
        component: Login,
        meta:{title:"Game Rank - Register"}
    },
    {
        path: "/content",
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
})


export default router;
