<template>
    <v-container>
        <v-row>
            <v-col>
                <v-text-field v-model="newHandle" label="Add Handle" @keyup.enter="addHandle"></v-text-field>
                <v-btn @click="addHandle">Add</v-btn>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-list>
                    <v-list-item v-for="(handle, index) in handles" :key="index">
                        <v-row>
                            <v-col>{{ handle }}</v-col>
                            <v-col cols="auto">
                                <v-btn icon @click="removeHandle(index)">
                                    <v-icon>mdi-delete</v-icon>
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-list-item>
                </v-list>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
    name: "Setting",
    setup() {
        const newHandle = ref("");
        const handles = ref<string[]>(JSON.parse(localStorage.getItem("handles") || "[]"));

        const addHandle = () => {
            if (newHandle.value && !handles.value.includes(newHandle.value)) {
                handles.value.push(newHandle.value);
                localStorage.setItem("handles", JSON.stringify(handles.value));
                newHandle.value = "";
            }
        };

        const removeHandle = (index: number) => {
            handles.value.splice(index, 1);
            localStorage.setItem("handles", JSON.stringify(handles.value));
        };

        return {
            newHandle,
            handles,
            addHandle,
            removeHandle,
        };
    },
});
</script>

<style scoped>
/* 添加一些基本样式 */
</style>
