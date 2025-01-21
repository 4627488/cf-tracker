import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";

// 引入 Vuetify
import "vuetify/dist/vuetify.css";
import { createVuetify } from "vuetify";

// 引入 mdi 图标
import "@mdi/font/css/materialdesignicons.css";

import { md3 } from "vuetify/blueprints";

// 引入 Vue Router
import { createRouter, createWebHistory } from "vue-router";
import Heatmap from "./components/Heatmap.vue";
import Setting from "./components/Setting.vue";

const prefersDarkScheme = window.matchMedia(
  "(prefers-color-scheme: dark)",
).matches;

const vuetify = createVuetify({
  blueprint: md3,
  theme: {
    defaultTheme: prefersDarkScheme ? "dark" : "light",
    themes: {
      light: {
        dark: false,
        colors: {
          primary: "#1976D2",
          secondary: "#424242",
          accent: "#82B1FF",
          error: "#FF5252",
          info: "#2196F3",
          success: "#4CAF50",
          warning: "#FFC107",
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: "#2196F3",
          secondary: "#424242",
          accent: "#FF4081",
          error: "#FF5252",
          info: "#2196F3",
          success: "#4CAF50",
          warning: "#FFC107",
        },
      },
    },
  },
});

const routes = [
  { path: "/", component: Heatmap, name: "home" },
  { path: "/settings", component: Setting, name: "settings" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App)
  .use(vuetify) // 使用 Vuetify
  .use(router) // 使用 Vue Router
  .mount("#app");
