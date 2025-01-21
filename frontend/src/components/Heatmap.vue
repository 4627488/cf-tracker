<template>
  <v-col no-gutters>
    <UserCard v-for="user in users" :key="user.user" :user="user" />
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

    const fetchData = async () => {
      try {
        const response = await fetch("/api/user-data");
        const responseData = await response.json();
        const { lastUpdate, data } = responseData;

        users.value = data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    onMounted(fetchData);

    return {
      users,
    };
  },
});
</script>
