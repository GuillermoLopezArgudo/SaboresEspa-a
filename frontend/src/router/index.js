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
  { path: '/', component: MainPage, name:"/"},
  { path: '/login', component: LoginPage, name:"login"},
  { path: '/register', component: RegisterPage, name:"register" },
  { path: '/home', component: HomeRecipe, name:"home" },
  { path: '/create', component: CreateRecipe, name:"create" },
  { path: '/recipe', component: Recipe, name:"recipe", props: route => ({ id: route.query.id }) },
  { path: '/edite', component: EditeRecipe, name:"edite", props: route => ({ id: route.query.id }) },
  { path: '/profile', component: Profile, name:"profile"},
  { path: '/recipes_personal', component: PersonalRecipes, name:"recipes_personal"}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
