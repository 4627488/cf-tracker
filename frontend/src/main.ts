import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";

// 引入 Vuetify
import "vuetify/dist/vuetify.css";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

const vuetify = createVuetify({
  components,
  directives,
});

createApp(App)
  .use(vuetify) // 使用 Vuetify
  .mount("#app");
