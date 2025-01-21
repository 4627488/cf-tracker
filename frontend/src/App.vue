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

      <v-app-bar-title>Cafebabe's Codeforces Board 🥳 (CCB)</v-app-bar-title>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item title="Ranklist" to="/"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
      <Heatmap />
    </v-main>
  </v-app>
</template>