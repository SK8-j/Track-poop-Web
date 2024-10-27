import { createRouter, createWebHistory } from 'vue-router';
// import Login from '../views/Login.vue';
// import Register from '../views/Register.vue';
import HomePage from '../views/HomePage.vue';
import LoginRegisterContainer from '../views/auth.vue';
import ProfilePage from '@/views/ProfilePage.vue';

const routes = [
  {
    path: '/home',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginRegisterContainer,
    meta: { requiresAuth: false }, // 不需要登录
  },
  {
    path: '/register',
    name: 'Register',
    component: LoginRegisterContainer,
    meta: { requiresAuth: false }, // 不需要登录
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('user_id');
  if (to.name !== 'Login' && to.name !== 'Register' && !isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next();
  }
});


