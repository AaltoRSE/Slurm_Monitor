import { createApp } from "vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import Tooltip from "primevue/tooltip";
import ToastService from "primevue/toastservice";
import App from "@/App.vue";
import "./index.css";
import Aura from "@primeuix/themes/aura";
import router from "./router";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(PrimeVue, { theme: { preset: Aura }, ripple: true });
app.use(ToastService);

app.directive("tooltip", Tooltip);

app.mount("#app");
