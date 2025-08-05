<script setup lang="ts">
import { SelectRoot, type SelectRootProps } from 'reka-ui'

interface Props extends SelectRootProps {}

defineProps<Props>()
</script>

<template>
  <SelectRoot v-bind="$props">
    <slot />
  </SelectRoot>
</template>

<style>
  .select-root {
    margin-bottom: 20px;
  }
</style>