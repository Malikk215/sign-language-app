
<script setup lang="ts">
import { ref } from 'vue';

const user = ref({
  name: 'John Doe',
  email: 'johndoe@example.com',
});

const triedAlphabets = ref(['A', 'B', 'D', 'F', 'G']);
</script>

<template>
  <div class="p-6">
    <!-- User Profile Section -->
    <div class="mb-8 rounded-lg bg-white p-6 shadow-md dark:bg-gray-800">
      <h2 class="mb-4 text-2xl font-bold text-gray-900 dark:text-white">User Profile</h2>
      <p class="text-gray-700 dark:text-gray-300"><strong>Name:</strong> {{ user.name }}</p>
      <p class="text-gray-700 dark:text-gray-300"><strong>Email:</strong> {{ user.email }}</p>
    </div>

    <!-- History Section -->
    <div class="rounded-lg bg-white p-6 shadow-md dark:bg-gray-800">
      <h2 class="mb-4 text-2xl font-bold text-gray-900 dark:text-white">History: Alphabets You've Tried</h2>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="letter in triedAlphabets"
          :key="letter"
          class="inline-block rounded-full bg-blue-600 px-4 py-2 text-white text-lg font-semibold"
        >
          {{ letter }}
        </span>
      </div>
    </div>
  </div>
</template>
