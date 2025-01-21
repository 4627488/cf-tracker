<template>
  <v-list-item class="mx-auto user-card" :prepend-avatar="user.avatar"
    style="border: 1px solid #ccc; border-radius: 8px; max-width: fit-content; margin: 1rem 0;">
    <template v-slot:title>
      <div class="d-flex">
        <span :style="{ fontWeight: 'bold', fontSize: '1.25rem', marginRight: '0.5rem' }">{{ index + 1 }}.</span>
        <a :href="`https://codeforces.com/profile/${user.user}`" target="_blank"
          :style="{ color: user.color, fontWeight: 'bold', textDecoration: 'none', fontSize: '1.25rem', marginRight: '0.5rem' }">{{
            user.user }}</a>
        <v-chip color="primary">{{ user.total }}</v-chip>
      </div>
    </template>

    <template v-slot:subtitle>
      <div style="display: flex; align-items: center; flex-wrap: wrap;">
        <v-sheet v-for="(day, index) in user.days" :key="index" class="heatmap-row">
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
    index: {
      type: Number,
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
  justify-content: flex-start;
}

.cell {
  width: 1.5rem;
  /* 20px */
  height: 1.5rem;
  /* 20px */
  margin-right: 0.125rem;
  /* 2px */
  text-align: center;
  line-height: 1.5rem;
  /* 20px */
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
