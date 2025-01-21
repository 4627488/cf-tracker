<template>
  <v-list-item class="mx-auto user-card" :prepend-avatar="user.avatar" :subtitle="user.group">
    <template v-slot:title>
      <a :href="`https://codeforces.com/profile/${user.user}`" target="_blank"
        :style="{ color: user.color, fontWeight: 'bold', textDecoration: 'none' }">{{ user.user }}</a>
      <span> ({{ user.total }})</span>
    </template>
    <template v-slot:subtitle>
      <v-container class="heatmap-container" :id="'heatmap-container-' + user.user">
        <v-row>
          <v-sheet v-for="(day, index) in user.days" :key="index" class="heatmap-row">
            <v-tooltip location="top"> <template v-slot:activator="{ props }">
                <div class="cell" :class="'cell-' + Math.min(day.length, 6)" @click="showPopup(day)" v-bind="props">
                  {{ day.length }}
                </div>
              </template>
              <span>{{ calculateDate(index) }}</span>
            </v-tooltip>
          </v-sheet>
        </v-row>
      </v-container>
    </template>
  </v-list-item>

  <v-dialog v-model="dialog" max-width="500">
    <v-card-title>{{ dialogDate }}</v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item v-for="problem in dialogProblems" :key="problem.link">
          <v-list-item-title>
            <a :href="problem.link" target="_blank">{{ problem.problem }}</a>
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { VListItem, VListItemTitle } from 'vuetify/components';

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
  name: "UserCard",
  props: {
    user: {
      type: Object as () => User,
      required: true,
    },
  },
  setup() {
    const dialog = ref(false);
    const dialogDate = ref("");
    const dialogProblems = ref(Array<{ link: string, problem: string }>());

    const showPopup = (day: { contestId: number; index: string; problem: string }[]) => {
      if (day.length > 0) {
        dialogProblems.value = day.map((d) => ({
          link: `https://codeforces.com/${Number(d.contestId) > 100000 ? "gym" : "contest"}/${d.contestId}/problem/${d.index}`,
          problem: `${d.contestId}${d.index} ${d.problem}`,
        }));
        dialog.value = true;
      }
    };

    const closePopup = () => {
      dialog.value = false;
    };

    const calculateDate = (index: number) => {
      const date = new Date();
      index = 30 - index - 1;
      date.setDate(date.getDate() - index);
      return date.toDateString().slice(4, 10);
    };

    return {
      dialog,
      dialogDate,
      dialogProblems,
      showPopup,
      closePopup,
      calculateDate,
    };
  },
});
</script>

<style>
.heatmap-container {
  display: flex;
  flex-wrap: wrap;
}

.heatmap-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.cell {
  width: 20px;
  height: 20px;
  margin-right: 2px;
  text-align: center;
  line-height: 20px;
  cursor: pointer;
}

.cell-0 {
  background-color: #ebedf0;
}

.cell-1 {
  background-color: #c6e48b;
}

.cell-2 {
  background-color: #7bc96f;
}

.cell-3 {
  background-color: #239a3b;
}

.cell-4 {
  background-color: #196127;
}

.cell-5 {
  background-color: #0f4c1a;
}

.cell-6 {
  background-color: #003300;
}
</style>
