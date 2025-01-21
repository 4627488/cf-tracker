<template>
  <div class="heatmap-container">
    <v-overlay :model-value="overlay" class="align-center justify-center" contained>
      <v-progress-circular color="primary" size="64" indeterminate></v-progress-circular>
    </v-overlay>
    <v-col v-if="!overlay">
      <v-list>
        <UserCard v-for="(handle, index) in handles" :key="handle" :handle="handle" :index="index"
          @user-data="updateUserData" />
      </v-list>
      <v-container>
        {{ handles.length }} users, last update: {{ new Date(lastUpdate).toLocaleString() }}
      </v-container>
    </v-col>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from "vue";
import UserCard from "./UserCard.vue";
import { VContainer } from "vuetify/components";

export default defineComponent({
  name: "Heatmap",
  components: {
    UserCard,
    VContainer,
  },
  setup() {
    const handles = ref<string[]>(JSON.parse(localStorage.getItem("handles") || "[]"));
    const lastUpdate = ref("");
    const overlay = ref(true);
    const usersStars = ref<{ [key: string]: { total: number } }>({});

    const sortHandles = () => {
      handles.value = handles.value.slice().sort((a, b) => {
        const userA = usersStars.value[a];
        const userB = usersStars.value[b];
        console.log(userA, userB);
        // 从大到小排序
        return (userB?.total || 0) - (userA?.total || 0);
      });
    };

    watch(usersStars, sortHandles, { deep: true });

    const updateUserData = (handle: string, data: { total: number }) => {
      console.log(`Updating data for handle: ${handle}`, data);
      usersStars.value[handle] = data;
    };

    const fetchData = async () => {
      try {
        lastUpdate.value = new Date().toISOString();
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        overlay.value = false;
      }
    };

    onMounted(fetchData);

    return {
      overlay,
      handles,
      lastUpdate,
      updateUserData,
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
