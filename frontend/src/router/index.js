import {createRouter, createWebHistory} from "vue-router";
import Login from "../view/login_user.vue";

const routes = [
    {
        path: "/login",
        component: Login

    }
];

const router = createRouter({
    history:createWebHistory(),
    routes
})


export default router;
