import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import { useAuthStore } from "./stores/auth";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

axios.defaults.baseURL = "http://localhost:8000";
axios.defaults.withCredentials = true;

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

app.use(pinia);
app.use(router);
app.use(Toast, {
  position: "bottom-right",
  timeout: 4000,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  hideProgressBar: false,
});

app.mount("#app");

const authStore = useAuthStore();
if (authStore.jwtToken) {
  authStore.fetchUser();
}
