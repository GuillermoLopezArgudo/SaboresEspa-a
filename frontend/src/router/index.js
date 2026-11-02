import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import CreateRecipe from '@/components/CreateRecipe.vue';
import Recipe from '@/components/RecipeView.vue';
import EditRecipe from '@/components/EditRecipe.vue';
import Profile from '@/components/ProfileUser.vue';
import MainPage from '@/components/MainPage.vue';
import HomeRecipe from '@/components/HomeRecipe.vue';
import PersonalRecipes from '@/components/PersonalRecipes.vue';
import { clearSession, isTokenValid } from '../api';

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
    path: '/edit',
    component: EditRecipe,
    name: 'edit',
    meta: { requiresAuth: true },
    props: (route) => ({ id: route.query.id }),
  },
  // alias tipográfico legacy
  {
    path: '/edite',
    redirect: (to) => ({ path: '/edit', query: to.query }),
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
  const valid = isTokenValid(token);
  if (token && !valid) {
    clearSession();
  }
  if (to.meta.requiresAuth && !valid) {
    return { name: 'login', query: { redirect: to.fullPath } };
  }
  if (to.meta.guest && valid && (to.name === 'login' || to.name === 'register')) {
    return { name: 'home' };
  }
  return true;
});

export default router;
