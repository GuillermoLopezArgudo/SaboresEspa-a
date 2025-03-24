import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import HomePage from '../components/HomePage.vue';
import CreateRecipe from '@/components/CreateRecipe.vue';

const routes = [
  { path: '/login', component: LoginPage, name:"login"},
  { path: '/register', component: RegisterPage, name:"register" },
  { path: '/home', component: HomePage, name:"home" },
  { path: '/create', component: CreateRecipe, name:"create" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
