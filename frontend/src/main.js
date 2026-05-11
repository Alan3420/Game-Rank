import { createApp } from "vue"
import App from "./base/App.vue"
import router from "./router/index.js"
import 'primeicons/primeicons.css'
import "./style.css"

import PrimeVue from "primevue/config"

const app = createApp(App)

app.use(router)

app.use(PrimeVue)

app.mount("#app")