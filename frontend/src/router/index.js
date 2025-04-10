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
  { path: '/', component: MainPage, name:"/", meta: { title: "Inicio" }},
  { path: '/login', component: LoginPage, name:"login", meta: { title: "Iniciar sesión" }},
  { path: '/register', component: RegisterPage, name:"register", meta: { title: "Registrarse" }},
  { path: '/home', component: HomeRecipe, name:"home", meta: { title: "Recetas" } },
  { path: '/create', component: CreateRecipe, name:"create", meta: { title: "Crear Receta" } },
  { path: '/recipe', component: Recipe, name:"recipe", meta: { title: "Ver Receta" }, props: route => ({ id: route.query.id }) },
  { path: '/edite', component: EditeRecipe, name:"edite", meta: { title: "Editar Receta" }, props: route => ({ id: route.query.id }) },
  { path: '/profile', component: Profile, name:"profile", meta: { title: "Mi Perfil" }},
  { path: '/recipes_personal', component: PersonalRecipes, name:"recipes_personal", meta: { title: "Mis Recetas" }}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const defaultTitle = "Frontend";
  document.title = to.meta.title || defaultTitle;
  next();
});

export default router;
