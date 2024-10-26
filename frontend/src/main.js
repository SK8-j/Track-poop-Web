import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 确保这个路径与刚才创建的文件匹配
import store from './store';

const app = createApp(App);
app.use(router);
app.use(store);
app.mount('#app');
