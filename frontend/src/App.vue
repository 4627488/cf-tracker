<script setup lang="ts">
import { ref, watchEffect } from "vue";
import Heatmap from "./components/Heatmap.vue";
document.title = "Codeforce Daily Tracker";

const drawer = ref(true);

watchEffect(() => {
  drawer.value = window.innerWidth >= 1024;
});
</script>

<template>
  <v-app class="rounded rounded-md">
    <v-app-bar color="primary">
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      </template>

      <v-app-bar-title>Cafebabe's Codeforces Board 🥳 <v-chip>CCB</v-chip></v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn icon href="https://github.com/4627488/cf-tracker" target="_blank">
        <v-icon>mdi-github</v-icon>
      </v-btn>
    </v-app-bar>


    <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
      <Heatmap />
    </v-main>

    <v-footer app>
      <v-row justify="center" no-gutters>
        <v-col class="text-center mt-4" cols="12">
          {{ new Date().getFullYear() }} - <strong>Caizi Jiangnan</strong> | Powered by <strong>Vuetify</strong>

        </v-col>
      </v-row>
    </v-footer>

    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item title="Ranklist" to="/"></v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-app>
</template>