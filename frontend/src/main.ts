import { createApp } from "vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import Tooltip from "primevue/tooltip";
import ToastService from "primevue/toastservice";
import App from "@/App.vue";
import Aura from "@primeuix/themes/aura";

const stylePreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: "#f2eef7",
      100: "#dcd4e5",
      200: "#c5b9d3",
      300: "#ae9fc1",
      400: "#9784af",
      500: "#493f61",
      600: "#3e3552",
      700: "#322b43",
      800: "#272234",
      900: "#1c1825",
    },
    colorScheme: {
      dark: {
        surface: {
          0: "#ffffff",
          50: "{neutral.50}",
          100: "{neutral.100}",
          200: "{neutral.200}",
          300: "{neutral.300}",
          400: "{neutral.400}",
          500: "{neutral.500}",
          600: "{neutral.600}",
          700: "{neutral.700}",
          800: "{neutral.800}",
          900: "{neutral.900}",
          950: "{neutral.950}",
        },
      },
    },
  },
});

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(PrimeVue, { theme: { preset: stylePreset }, ripple: true });

import "./index.css";
import { definePreset } from "@primeuix/themes";

app.use(ToastService);

app.directive("tooltip", Tooltip);

app.mount("#app");
