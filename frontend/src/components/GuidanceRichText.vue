<template>
  <Card class="mb-4">
    <CardHeader class="pb-3">
      <CardTitle class="text-base">{{ $t('guidance.title') }}</CardTitle>
    </CardHeader>
    <CardContent>
      <article
        class="prose prose-sm max-w-none text-foreground prose-headings:font-semibold prose-p:leading-6 prose-li:leading-6"
        v-html="htmlContent"
      />
      <div v-if="timestamp" class="mt-3 text-xs text-muted-foreground">
        {{ timestamp }}
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Props {
  content: string
  timestamp?: string
}

const props = withDefaults(defineProps<Props>(), {
  timestamp: '',
})

const htmlContent = computed(() => {
  return marked.parse(props.content || '') as string
})
</script>
