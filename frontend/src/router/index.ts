import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Profile from '../views/Profile.vue'
import About from '../views/About.vue'
import TopicSpeaking from '../views/TopicSpeaking.vue'
import MockExam from '../views/MockExam.vue'
import ExamStats from '../views/ExamStats.vue'
import PersonalizedPractice from '../views/PersonalizedPractice.vue'
import ErrorNotebook from '../views/ErrorNotebook.vue'
import QuestionBank from '../views/QuestionBank.vue'
import PscPartView from '../views/PscPartView.vue'

const VALID_TYPES = ['character', 'word', 'sentence', 'article'] as const
const VALID_PSC_PARTS = ['singleCharacterReading', 'wordReading', 'choiceJudgment', 'passageReading'] as const

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: () => ({ path: '/profile' }),
    },
    {
      path: '/question-type/:type',
      name: 'question-type',
      component: Home,
      beforeEnter(to, _from, next) {
        const type = to.params.type as string
        if (VALID_TYPES.includes(type as (typeof VALID_TYPES)[number])) {
          next()
        } else {
          next({ path: '/question-type/word' })
        }
      },
    },
    {
      path: '/topic-speaking',
      name: 'topic-speaking',
      component: TopicSpeaking,
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
    },
    {
      path: '/about',
      name: 'about',
      component: About,
    },
    {
      path: '/mock-exam',
      name: 'mock-exam',
      component: MockExam,
    },
    {
      path: '/exam-stats',
      name: 'exam-stats',
      component: ExamStats,
    },
    {
      path: '/personalized-practice',
      name: 'personalized-practice',
      component: PersonalizedPractice,
    },
    {
      path: '/error-notebook',
      name: 'error-notebook',
      component: ErrorNotebook,
    },
    {
      path: '/question-bank',
      name: 'question-bank',
      component: QuestionBank,
    },
    {
      path: '/psc/:partId',
      name: 'psc-part',
      component: PscPartView,
      beforeEnter(to, _from, next) {
        const partId = to.params.partId as string
        if (VALID_PSC_PARTS.includes(partId as (typeof VALID_PSC_PARTS)[number])) {
          next()
        } else {
          next({ path: '/topic-speaking' })
        }
      },
    },
  ],
})

export default router
