import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';

// 定义路由规则
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  // 你可以根据需要添加其他路由
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
