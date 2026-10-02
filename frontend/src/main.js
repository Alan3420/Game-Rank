import { createApp } from "vue";
import App from "./base/App.vue";
import router from "./router/index.js";
import PrimeVue from "primevue/config";
import { activable } from "./utils/activable.js";

import 'primeicons/primeicons.css';
import "./style.css";


const app = createApp(App);

app.use(router);
app.use(PrimeVue);
app.directive("activable", activable);

app.mount("#app");
