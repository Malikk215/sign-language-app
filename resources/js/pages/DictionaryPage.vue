
<script setup lang="ts">
import { ref } from 'vue';

const alphabet = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i));
</script>

<template>
  <div class="p-6">
    <h1 class="mb-6 text-3xl font-bold text-center text-gray-800 dark:text-white">Sign Language Dictionary</h1>
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
      <div
        v-for="letter in alphabet"
        :key="letter"
        class="rounded-lg border border-gray-300 bg-white p-4 text-center shadow hover:shadow-md dark:border-gray-700 dark:bg-gray-800"
      >
        <span class="text-2xl font-bold text-gray-900 dark:text-white">{{ letter }}</span>
      </div>
    </div>
  </div>
</template>
