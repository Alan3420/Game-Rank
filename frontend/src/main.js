// Punto de entrada de la app Vue.
// Aqui se monta el componente raiz, se registra el router y los plugins
// que necesita la app antes de pintar nada en el navegador.

import { createApp } from "vue";
import App from "./base/App.vue";
import router from "./router/index.js";
import PrimeVue from "primevue/config";

// Estilos globales: iconos de PrimeIcons y nuestra hoja de estilos base.
import 'primeicons/primeicons.css';
import "./style.css";


const app = createApp(App);

app.use(router);
app.use(PrimeVue);

app.mount("#app");
