import { createApp } from "vue";
import "./styles.css";
import "./w3.css";
import "./imported.css"
import App from "./App.vue";
import rate from 'vue-rate';
import 'vue-rate/dist/vue-rate.css';

createApp(App).use(rate).mount("#app");
