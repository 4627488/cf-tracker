<template>
  <v-list-item class="mx-auto user-card" :prepend-avatar="user?.avatar"
    style="border: 1px solid #ccc; border-radius: 8px; max-width: fit-content; margin: 1rem 0;">
    <v-overlay :model-value="overlay" class="align-center justify-center" contained>
      <v-progress-circular color="primary" size="64" indeterminate></v-progress-circular>
    </v-overlay>
    <template v-slot:title>
      <div class="d-flex">
        <span :style="{ fontWeight: 'bold', fontSize: '1.25rem', marginRight: '0.5rem' }">{{ index + 1 }}.</span>
        <a :href="`https://codeforces.com/profile/${user?.user}`" target="_blank"
          :style="{ color: user?.color, fontWeight: 'bold', textDecoration: 'none', fontSize: '1.25rem', marginRight: '0.5rem' }">{{
            user?.user }}</a>
        <v-spacer></v-spacer>
        Σ={{ user?.total }}
      </div>
    </template>

    <template v-slot:subtitle>
      <div style="display: flex; align-items: center; flex-wrap: wrap;">
        <v-sheet v-for="(day, index) in user?.days" :key="index" class="heatmap-row">
          <v-tooltip location="top"> <template v-slot:activator="{ props }">
              <div class="cell" :class="'cell-' + Math.min(day.length, 6)" @click="showPopup(day)" v-bind="props">
                {{ day.length }}
              </div>
            </template>
            <span>{{ calculateDate(index) }}</span>
          </v-tooltip>
        </v-sheet>
      </div>
    </template>
  </v-list-item>
  <v-dialog v-model="dialog" width="auto">
    <v-card max-width="400" prepend-icon="mdi-update" title="Problems">
      <v-card-text>
        <v-list>
          <v-list-item v-for="problem in dialogProblems" :key="problem.link">
            <v-list-item-title>
              <a :href="problem.link" target="_blank">{{ problem.problem }}</a>
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card-text>
      <template v-slot:actions>
        <v-btn class="ms-auto" text="Ok" @click="dialog = false"></v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import type { PropType } from "vue";

const CODEFORCES_API_URL = "https://codeforces.com/api/user.status?handle={}&from=1&count=300";
const CODEFORCES_USER_INFO_URL = "https://codeforces.com/api/user.info?handles={}";
const rankColors = {
  newbie: "#808080",
  pupil: "#008000",
  specialist: "#03a89e",
  expert: "#0000ff",
  "candidate master": "#aa00aa",
  master: "#ff8c00",
  "international master": "#ff8c00",
  grandmaster: "#ff0000",
  "international grandmaster": "#ff0000",
  "legendary grandmaster": "#ff0000",
};

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
    handle: {
      type: String as PropType<string>,
      required: true,
    },
    index: {
      type: Number as PropType<number>,
      required: true,
    },
  },
  emits: ["user-data"],
  setup(props, { emit }) {
    const user = ref<User>({
      user: props.handle,
      avatar: "/vite.svg",
      color: "",
      group: "",
      total: 0,
      lastUpdate: "",
      days: Array.from({ length: 30 }, () => []),
    });
    const overlay = ref(true);
    const dialog = ref(false);
    const dialogDate = ref("");
    const dialogProblems = ref(Array<{ link: string, problem: string }>());

    const fetchUserInfo = async (handle: string) => {
      const response = await fetch(CODEFORCES_USER_INFO_URL.replace("{}", handle));
      if (!response.ok) throw new Error("Failed to fetch user info");
      const data = await response.json();
      return data.result[0];
    };

    const fetchUserSubmissions = async (handle: string) => {
      const response = await fetch(CODEFORCES_API_URL.replace("{}", handle));
      if (!response.ok) throw new Error("Failed to fetch user submissions");
      const data = await response.json();
      return data.result;
    };

    const loadUserData = async () => {
      try {
        const userInfo = await fetchUserInfo(props.handle);
        user.value.avatar = userInfo.titlePhoto;
        user.value.color = rankColors[(userInfo.rank?.toLowerCase() as keyof typeof rankColors) || "newbie"];
        const submissions = await fetchUserSubmissions(props.handle);
        const tonight = new Date();
        tonight.setHours(23, 59, 59, 999);
        const days: Array<Array<{ contestId: number; index: string; problem: string }>> = Array.from({ length: 30 }, () => []);
        const uniqueProblems = new Set();
        submissions.forEach((submission: any) => {
          if (submission.verdict !== "OK") return;
          const problemId = `${submission.problem.contestId}-${submission.problem.index}`;
          if (uniqueProblems.has(problemId)) return;
          uniqueProblems.add(problemId);
          const submissionTime = new Date(submission.creationTimeSeconds * 1000);
          const dayIndex = Math.floor((tonight.getTime() - submissionTime.getTime()) / (1000 * 60 * 60 * 24));
          if (dayIndex < 30) {
            days[dayIndex].push({
              problem: submission.problem.name,
              contestId: submission.problem.contestId,
              index: submission.problem.index,
            });
          }
        });
        user.value = {
          user: userInfo.handle,
          avatar: userInfo.titlePhoto,
          color: rankColors[(userInfo.rank?.toLowerCase() as keyof typeof rankColors) || "newbie"],
          group: "default", // Replace with actual group if available
          days,
          lastUpdate: new Date().toISOString(),
          total: days.reduce((sum, day) => sum + day.length, 0),
        };
        emit("user-data", props.handle, { total: user.value.total });
      } catch (error) {
        console.error("Error fetching user info:", error);
      }
      overlay.value = false;
    };

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

    onMounted(loadUserData);

    return {
      user,
      overlay,
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

<style scoped>
.heatmap-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.cell {
  width: 1.5rem;
  height: 1.5rem;
  margin-right: 0.125rem;
  text-align: center;
  line-height: 1.5rem;
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

.user-card .v-list-item__avatar {
  width: 2rem;
  height: 2rem;
}

.user-card .v-list-item__title {
  font-size: 1.25rem;
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
  .container {
    background-color: #1e1e1e;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }

  #heatmap-container {
    background-color: #1e1e1e;
    border: 1px solid #333;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }

  #last-update {
    color: #aaaaaa;
  }

  .cell {
    color: #e0e0e0;
  }

  .cell-0 {
    background-color: #333;
  }

  .cell-1 {
    background-color: #4caf50;
  }

  .cell-2 {
    background-color: #388e3c;
  }

  .cell-3 {
    background-color: #2e7d32;
  }

  .cell-4 {
    background-color: #1b5e20;
  }

  .cell-5 {
    background-color: #003300;
  }

  .cell-6 {
    background-color: #002200;
  }
}
</style>
