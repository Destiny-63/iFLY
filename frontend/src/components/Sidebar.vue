<template>
  <Sidebar variant="sidebar" collapsible="icon">
    <SidebarHeader>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton size="lg">
            <div class="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
              <BookOpen class="size-4" />
            </div>
            <div class="grid flex-1 text-left text-sm leading-tight">
              <span class="truncate font-semibold">{{ $t('common.appName') }}</span>
              <span class="truncate text-xs">{{ $t('common.appSubtitle') }}</span>
            </div>
            <ChevronsUpDown class="ml-auto size-4" />
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarHeader>

    <SidebarContent>
      <!-- 主导航 -->
      <SidebarGroup>
        <SidebarGroupLabel>{{ $t('sidebar.mainNav') }}</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton
                :is-active="route.path === '/profile'"
                @click="router.push('/profile')"
              >
                <User class="size-4" />
                <span>{{ $t('profile.title') }}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>

      <SidebarSeparator />

      <!-- 模拟考试 -->
      <SidebarGroup>
        <SidebarGroupLabel>{{ $t('sidebar.mockExam') }}</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton
                :is-active="route.path === '/mock-exam'"
                @click="router.push('/mock-exam')"
              >
                <FileCheck class="size-4" />
                <span>{{ $t('sidebar.startExam') }}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton
                :is-active="route.path === '/exam-stats'"
                @click="router.push('/exam-stats')"
              >
                <BarChart3 class="size-4" />
                <span>{{ $t('sidebar.examStats') }}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>

      <SidebarSeparator />

      <!-- 专项训练 -->
      <SidebarGroup>
        <SidebarGroupLabel>{{ $t('sidebar.specializedTraining') }}</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem
              v-for="type in questionTypes"
              :key="type.id"
            >
              <SidebarMenuButton
                :is-active="route.path.startsWith('/question-type/') && currentType === type.id"
                @click="navigateToType(type.id)"
              >
                <component :is="typeIconMap[type.id] ?? BookOpen" class="size-4" />
                <span>{{ $t(`sidebar.${type.id}`) }}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>

      <SidebarSeparator />

      <!-- 错题本 -->
      <SidebarGroup>
        <SidebarGroupLabel>{{ $t('sidebar.errorNotebook') }}</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton
                :is-active="route.path === '/error-notebook'"
                @click="router.push('/error-notebook')"
              >
                <BookMarked class="size-4" />
                <span>{{ $t('sidebar.errorNotebookList') }}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>

      <SidebarSeparator />

      <!-- 题库 -->
      <SidebarGroup>
        <SidebarGroupLabel>{{ $t('sidebar.questionBank') }}</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton
                :is-active="route.path === '/psc/singleCharacterReading'"
                @click="router.push('/psc/singleCharacterReading')"
              >
                <Type class="size-4" />
                <span>{{ $t('sidebar.singleCharacterReading') }}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton
                :is-active="route.path === '/psc/wordReading'"
                @click="router.push('/psc/wordReading')"
              >
                <MessageSquareText class="size-4" />
                <span>{{ $t('sidebar.wordReading') }}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton
                :is-active="route.path === '/psc/choiceJudgment'"
                @click="router.push('/psc/choiceJudgment')"
              >
                <ListChecks class="size-4" />
                <span>{{ $t('sidebar.choiceJudgment') }}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton
                :is-active="route.path === '/psc/passageReading'"
                @click="router.push('/psc/passageReading')"
              >
                <FileText class="size-4" />
                <span>{{ $t('sidebar.passageReading') }}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton
                :is-active="route.path === '/topic-speaking'"
                @click="router.push('/topic-speaking')"
              >
                <Mic class="size-4" />
                <span>{{ $t('sidebar.topicSpeaking') }}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>

      <SidebarSeparator />

      <!-- 关于我们 -->
      <SidebarGroup>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton
                :is-active="route.path === '/about'"
                @click="router.push('/about')"
              >
                <Info class="size-4" />
                <span>{{ $t('sidebar.aboutUs') }}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </SidebarContent>

    <SidebarSeparator />

    <SidebarFooter>
      <SidebarMenu>
        <SidebarMenuItem>
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <SidebarMenuButton size="lg" class="w-full">
                <Avatar class="h-8 w-8 rounded-lg">
                  <AvatarImage :src="userData.avatarUrl" :alt="userData.name" />
                  <AvatarFallback class="rounded-lg flex items-center justify-center">
                    <User class="size-4 text-muted-foreground" />
                  </AvatarFallback>
                </Avatar>
                <div class="grid flex-1 text-left text-sm leading-tight">
                  <span class="truncate font-semibold">{{ userData.name }}</span>
                  <span class="truncate text-xs text-muted-foreground">{{ userData.email }}</span>
                </div>
                <ChevronUp class="ml-auto size-4" />
              </SidebarMenuButton>
            </DropdownMenuTrigger>
            <DropdownMenuContent class="w-56" side="bottom" align="end">
              <DropdownMenuLabel>{{ $t('sidebar.myAccount') }}</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem @click="router.push('/profile')">
                <User class="mr-2 size-4" />
                <span>{{ $t('sidebar.profile') }}</span>
              </DropdownMenuItem>
              <DropdownMenuItem @click="showSettings = true">
                <Settings class="mr-2 size-4" />
                <span>{{ $t('sidebar.settings') }}</span>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <BarChart3 class="mr-2 size-4" />
                <span>{{ $t('sidebar.learningStats') }}</span>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <LogOut class="mr-2 size-4" />
                <span>{{ $t('sidebar.logout') }}</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </SidebarMenuItem>
      </SidebarMenu>
      <div class="px-2 pb-1 text-xs text-muted-foreground">
        {{ $t(`sidebar.level_${userData.levelKey || 'novice'}`) }}
      </div>
    </SidebarFooter>

    <SidebarRail />
  </Sidebar>
  <SettingsDialog :open="showSettings" @update:open="showSettings = $event" />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  BookOpen,
  ChevronUp,
  ChevronsUpDown,
  FileText,
  MessageSquareText,
  FileCheck,
  BookMarked,
  Type,
  Mic,
  ListChecks,
  AlignLeft,
  User,
  Settings,
  BarChart3,
  LogOut,
  Info,
} from 'lucide-vue-next'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  SidebarSeparator,
} from '@/components/ui/sidebar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import SettingsDialog from '@/components/SettingsDialog.vue'
import { questionTypes, userData } from '@/data/mock'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()

const currentType = computed(() => {
  const t = route.params.type as string
  return t === 'character' || t === 'word' || t === 'sentence' || t === 'article' ? t : 'word'
})

const typeIconMap = {
  character: Type,
  word: MessageSquareText,
  sentence: AlignLeft,
  article: FileText,
} as const

const navigateToType = (typeId: string) => {
  const valid = ['character', 'word', 'sentence', 'article'].includes(typeId) ? typeId : 'word'
  router.push({ path: `/question-type/${valid}` })
}

const showSettings = ref(false)
</script>
