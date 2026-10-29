<template>
  <div class="flex items-center justify-center p-4">
    <div class="relative h-8 w-8">
      <div class="absolute h-8 w-8 animate-spin rounded-full border-4 border-muted border-t-primary"></div>
    </div>
    <span v-if="text" class="ml-2 text-sm text-muted-foreground">{{ text }}</span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  text?: string
}

withDefaults(defineProps<Props>(), {
  text: '',
})
</script>
