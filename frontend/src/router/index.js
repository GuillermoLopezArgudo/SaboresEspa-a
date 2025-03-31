import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import HomePage from '../components/HomePage.vue';
import CreateRecipe from '@/components/CreateRecipe.vue';
import RecipeView from '@/components/RecipeViewHome.vue';
import Recipe from '@/components/Recipe.vue';
import RecipesIndex from '@/components/RecipesViewIndex.vue';
import EditeRecipe from '@/components/EditeRecipe.vue';

const routes = [
  { path: '/', component: RecipesIndex, name:"/"},
  { path: '/login', component: LoginPage, name:"login"},
  { path: '/register', component: RegisterPage, name:"register" },
  { path: '/home', component: HomePage, name:"home" },
  { path: '/create', component: CreateRecipe, name:"create" },
  { path: '/recipes', component: RecipeView, name:"recipes" },
  { path: '/recipe', component: Recipe, name:"recipe", props: route => ({ id: route.query.id }) },
  { path: '/edite', component: EditeRecipe, name:"edite", props: route => ({ id: route.query.id }) },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
