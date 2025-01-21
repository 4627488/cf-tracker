<template>
  <v-col>
    <v-list>
      <UserCard v-for="(user) in users" :key="user.user" :user="user" />
    </v-list>
    <v-container>
      <span>Last update: {{ new Date(lastUpdate).toLocaleString() }}
      </span>
    </v-container>
  </v-col>
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
    const fetchData = async () => {
      try {
        const response = await fetch("/api/user-data");
        const responseData = await response.json();
        const { lastUpdate: update, data } = responseData;
        lastUpdate.value = update;
        users.value = data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    onMounted(fetchData);

    return {
      users,
      lastUpdate,
    };
  },
});
</script>

<style scoped>
.user-card-container {
  display: flex;
  align-items: center;
}

.user-card-container span {
  margin-right: 0.625rem;
  /* 10px */
  font-size: 1rem;
  /* 16px */
  /* 增加字体大小 */
}
</style>
