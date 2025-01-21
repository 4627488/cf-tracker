<template>
  <v-card class="user-card">
    <v-row>
      <v-col cols="4" class="d-flex align-items-center">
        <v-avatar class="mr-3">
          <img :src="user.avatar" :alt="`${user.user} avatar`" />
        </v-avatar>
        <div>
          <a
            :href="`https://codeforces.com/profile/${user.user}`"
            target="_blank"
            :style="{ color: user.color }"
          >
            {{ user.user }}<span v-if="user.group !== 'official'">🌟</span>
          </a>
          <div>∑={{ user.total }}</div>
        </div>
      </v-col>
      <v-col cols="8">
        <div
          :id="`heatmap-container-${user.user}`"
          class="heatmap-container"
        ></div>
      </v-col>
    </v-row>
  </v-card>

  <v-dialog v-model="dialog" max-width="500">
    <v-card>
      <v-card-title>{{ dialogDate }}</v-card-title>
      <v-card-text>
        <pre>{{ dialogProblems }}</pre>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="closePopup">关闭</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import * as d3 from "d3";

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
  setup(props) {
    const dialog = ref(false);
    const dialogDate = ref("");
    const dialogProblems = ref("");

    onMounted(() => {
      createHeatmap(props.user);
    });

    const createHeatmap = (user: User) => {
      const container = d3.select(`#heatmap-container-${user.user}`);
      const heatmapContainer = container
        .append("div")
        .attr("class", "heatmap-row")
        .style("display", "flex")
        .style("align-items", "center")
        .style("margin-bottom", "10px");

      user.days.forEach((day, index) => {
        const cellClass = `cell-${Math.min(day.length, 6)}`;
        const date = new Date();
        date.setDate(date.getDate() - index);
        const formattedDate = date.toISOString().split("T")[0];
        const problems = day
          .map(
            (d) =>
              `<a href="https://codeforces.com/${Number(d.contestId) > 100000 ? "gym" : "contest"}/${d.contestId}/problem/${d.index}" target="_blank" style="text-decoration: none;">${d.contestId}${d.index} ${d.problem}</a>`,
          )
          .join("<br>");

        const cell = heatmapContainer
          .append("div")
          .attr("class", `cell ${cellClass}`)
          .text(day.length);

        cell.on("click", () => showPopup(formattedDate, problems));
      });
    };

    const showPopup = (date: string, problems: string) => {
      dialogDate.value = date;
      dialogProblems.value = problems || "nothing";
      dialog.value = true;
    };

    const closePopup = () => {
      dialog.value = false;
    };

    return {
      dialog,
      dialogDate,
      dialogProblems,
      showPopup,
      closePopup,
    };
  },
});
</script>

<style scoped>
.user-card {
  margin-bottom: 20px;
}

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
