import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import CreateRecipe from '@/components/CreateRecipe.vue';
import Recipe from '@/components/RecipeView.vue';
import EditeRecipe from '@/components/EditeRecipe.vue';
import Profile from '@/components/ProfileUser.vue';
import MainPage from '@/components/MainPage.vue';
import HomeRecipe from '@/components/HomeRecipe.vue';
import PersonalRecipes from '@/components/PersonalRecipes.vue';

const routes = [
  { path: '/', component: MainPage, name: 'landing' },
  { path: '/login', component: LoginPage, name: 'login', meta: { guest: true } },
  { path: '/register', component: RegisterPage, name: 'register', meta: { guest: true } },
  { path: '/home', component: HomeRecipe, name: 'home', meta: { requiresAuth: true } },
  { path: '/create', component: CreateRecipe, name: 'create', meta: { requiresAuth: true } },
  {
    path: '/recipe',
    component: Recipe,
    name: 'recipe',
    props: (route) => ({ id: route.query.id }),
  },
  {
    path: '/edite',
    component: EditeRecipe,
    name: 'edite',
    meta: { requiresAuth: true },
    props: (route) => ({ id: route.query.id }),
  },
  { path: '/profile', component: Profile, name: 'profile', meta: { requiresAuth: true } },
  {
    path: '/recipes_personal',
    component: PersonalRecipes,
    name: 'recipes_personal',
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const token = localStorage.getItem('userToken');
  if (to.meta.requiresAuth && !token) {
    return { name: 'login', query: { redirect: to.fullPath } };
  }
  if (to.meta.guest && token && (to.name === 'login' || to.name === 'register')) {
    return { name: 'home' };
  }
  return true;
});

export default router;
