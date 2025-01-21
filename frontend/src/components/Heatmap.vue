<template>
  <div class="heatmap-container">
    <v-overlay :model-value="overlay" class="align-center justify-center">
      <v-progress-circular color="primary" size="64" indeterminate></v-progress-circular>
    </v-overlay>
    <v-col v-if="!overlay">
      <v-list>
        <UserCard v-for="(user, index) in users" :key="user.user" :user="user" :index="index" />
      </v-list>
      <v-container>
        <span>Last update: {{ new Date(lastUpdate).toLocaleString() }}</span>
      </v-container>
    </v-col>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import UserCard from "./UserCard.vue";
import { VContainer } from "vuetify/components";

interface User {
  user: string;
  avatar: string;
  color: string;
  group: string;
  total: number;
  lastUpdate: string;
  days: Array<Array<{ contestId: number; index: string; problem: string }>>;
}

export default defineComponent({
  name: "Heatmap",
  components: {
    UserCard,
    VContainer,
  },
  setup() {
    const users = ref<User[]>([]);
    const lastUpdate = ref("");
    const overlay = ref(true);

    const fetchData = async () => {
      try {
        const response = await fetch("/api/user-data");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const responseData = await response.json();
        const { lastUpdate: update, data } = responseData;
        lastUpdate.value = update;
        users.value = data;
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        overlay.value = false;
      }
    };

    onMounted(fetchData);

    return {
      overlay,
      users,
      lastUpdate,
    };
  },
});
</script>

<style scoped>
.heatmap-container {
  position: relative;
  width: 100%;
  height: 100%;
}

v-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.user-card-container {
  display: flex;
  align-items: center;
}

.user-card-container span {
  margin-right: 0.625rem;
  font-size: 1rem;
}
</style>
