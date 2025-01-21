<script setup lang="ts">
import Heatmap from "./components/Heatmap.vue";
document.title = "Codeforce Daily Tracker";
</script>

<template>
  <v-app>
    <v-main>
      <v-container class="d-flex justify-center">
        <Heatmap />
      </v-container>
    </v-main>
  </v-app>
</template>

<style>
/* 增加全局字体大小 */
.v-application {
  font-size: 16px;
}
</style>
