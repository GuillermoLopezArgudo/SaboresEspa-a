import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import HomePage from '../components/HomePage.vue';
import CreateRecipe from '@/components/CreateRecipe.vue';
import PersonalRecipe from '@/components/PersonalRecipes.vue';
import Recipe from '@/components/Recipe.vue';
import AllRecipes from '@/components/AllRecipes.vue';
import EditeRecipe from '@/components/EditeRecipe.vue';
import Profile from '@/components/Profile.vue';

const routes = [
  { path: '/', component: AllRecipes, name:"/"},
  { path: '/login', component: LoginPage, name:"login"},
  { path: '/register', component: RegisterPage, name:"register" },
  { path: '/home', component: HomePage, name:"home" },
  { path: '/create', component: CreateRecipe, name:"create" },
  { path: '/recipes_personal', component: PersonalRecipe, name:"recipes_personal" },
  { path: '/recipe', component: Recipe, name:"recipe", props: route => ({ id: route.query.id }) },
  { path: '/edite', component: EditeRecipe, name:"edite", props: route => ({ id: route.query.id }) },
  { path: '/profile', component: Profile, name:"profile"},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
