import { createApp } from "vue";
import App from "./base/App.vue";
import router from "./router/index.js";
import PrimeVue from "primevue/config";
import { activable } from "./utils/activable.js";

import 'primeicons/primeicons.css';
import "./style.css";
import "@fontsource/barlow/400.css";
import "@fontsource/barlow/500.css";
import "@fontsource/barlow/600.css";
import "@fontsource/barlow/700.css";
import "@fontsource/barlow-condensed/700.css";
import "@fontsource/barlow-condensed/800.css";
import "./styles/card-world.css";


const app = createApp(App);

app.use(router);
app.use(PrimeVue);
app.directive("activable", activable);

app.mount("#app");
