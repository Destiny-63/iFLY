<template>
  <div :class="cn('flex gap-4 p-4', isUser ? 'justify-end' : 'justify-start')">
    <div
      :class="cn(
        'flex max-w-[80%] flex-col gap-2',
        isUser ? 'items-end' : 'items-start'
      )"
    >
      <div
        :class="cn(
          'rounded-lg px-4 py-2',
          isUser
            ? 'bg-primary text-primary-foreground'
            : 'bg-muted text-muted-foreground'
        )"
      >
        <div v-if="isUser" class="text-sm">
          {{ content }}
        </div>
        <div v-else class="prose prose-sm max-w-none">
          <div class="whitespace-pre-wrap text-sm">{{ content }}</div>
        </div>
      </div>
      <span v-if="timestamp" class="text-xs text-muted-foreground">
        {{ timestamp }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { cn } from '@/lib/utils'

interface Props {
  content: string
  isUser?: boolean
  timestamp?: string
}

withDefaults(defineProps<Props>(), {
  isUser: false,
  timestamp: '',
})
</script>
