import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import LoginRegisterView from '@/views/LoginRegisterView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home/:username/:authority/:access_token',
      name: 'Home',
      component: HomeView,
      props: true,
      children: [
        {
          path: '',
          name: 'HomeContent',
          component: () => import('@/components/HomeContent.vue')
        },
        {
          path: 'tutorial-generate',
          name: 'TutorialGenerate',
          component: () => import('@/components/TutorialGenerate.vue'),
        },
        {
          path: 'tutorial-execute',
          name: 'TutorialExecute',
          component: () => import('@/components/TutorialExecute.vue'),
        },
        {
          path: 'log-management',
          name: 'LogManagement',
          component: () => import('@/components/LogManagement.vue'),
        },
        {
          path: 'guideline-generate',
          name: 'GuidelineGenerate',
          component: () => import('@/components/GuidelineGenerate.vue'),
        },
        {
          path: 'weather-entertainment',
          name: 'WeatherEntertainment',
          component: () => import('@/components/WeatherEntertainment.vue'),
        },
      ]
    },
    {
      path: '/',
      name: 'Login',
      component: LoginRegisterView,
      props: true
    },
    {
      path: '/speech',
      name: 'speech',
      component: () => import('@/components/SpeechToText.vue')
    },
    {
      path: '/text',
      name: 'text',
      component: () => import('@/components/TextToSpeech.vue')
    },
    {
      path:'/changeinfo/:viewNum?/:username?/:access_token?/:authority?',
      name: 'ChangeInfo',
      component: () => import('@/components/ChangeInfo.vue'),
      props:true
    }
  ],
});

export default router;
