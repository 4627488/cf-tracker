<script setup lang="ts">
import Heatmap from "./components/Heatmap.vue";
document.title = "Codeforce Daily Tracker";
</script>

<template>
  <v-app class="rounded rounded-md">
    <v-app-bar title="Cafebabe's Codeforces Board 🥳 (CCB)">
    </v-app-bar>

    <v-navigation-drawer>
      <v-list>
        <v-list-item title="Ranklist" to="/"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
      <Heatmap />
    </v-main>
  </v-app>
</template>