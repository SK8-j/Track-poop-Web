<template>
    <div class="homepage">
      <!-- 导入的导航栏组件 -->
      <NavBar />
  
      <!-- 图片大屏 -->
      <el-main class="main">
        <el-card class="banner-card" shadow="hover">
          <img class="banner-img" src="https://i.postimg.cc/fbG8ZRj6/DALL-E-2024-10-27-00-32-12-A-cute-and-colorful-cartoon-banner-illustration-themed-around-Poop-Bat.webp" alt="banner" />
        </el-card>
  
        <!-- 💩记录按钮 -->
        <div class="poop-battle">
          <h1>💩💩大作战</h1>
          <el-button type="primary" @click="recordPoop(0)">0 💩</el-button>
          <el-button type="success" @click="recordPoop(1)">1 💩</el-button>
          <el-button type="warning" @click="recordPoop(2)">2 💩</el-button>
        </div>
        <!-- 放点好玩的 -->
         <div class="oldprojector">
        <OldFilmProjector /></div>
        <!-- 用户信息区域 -->
      <el-card class="user-card" shadow="hover">
        <div class="user-info">
          <el-avatar size="large" src="your-avatar-image-url" />
          <p class="username">用户名: {{ userInfo.username }}</p>
          <p class="poop-count">💩数: {{ userInfo.poop_count }}</p>
          <el-button type="danger" @click="logout" class="logout-button">注销</el-button>
        </div>
      </el-card>
      </el-main>
    </div>
  </template>
  
  <script>
import NavBar from '../components/NavBar.vue';
import axios from 'axios';
import { showMessage } from '../utils/message';
import OldFilmProjector from '../components/OldFilmProjector.vue';

export default {
  name: 'HomePage',
  components: {
    NavBar,
    OldFilmProjector
  },
  data() {
    return {
      userInfo: {
        username: 'Loading...',
        poop_count: 0
      }
    };
  },
  mounted() {
    this.fetchUserInfo();
  },
  methods: {
    async fetchUserInfo() {
      try {
        const response = await axios.get('http://localhost:5000/user_info', { withCredentials: true });
        this.userInfo = response.data;
      } catch (error) {
        console.error('Error fetching user info:', error);
        showMessage('无法加载用户信息，请重新登录');
        this.$router.push('/login');
      }
    },
    async recordPoop(count) {
      try {
        const response = await axios.post('http://localhost:5000/record_poop', {
          poop_count: count
        }, { withCredentials: true });
        showMessage(response.data.message);
        // 重新获取用户信息以更新💩数
        this.fetchUserInfo();
      } catch (error) {
        console.error(error);
        showMessage('Error recording poop count!');
      }
    },
    async logout() {
      try {
        const response = await axios.post('http://localhost:5000/logout', {}, { withCredentials: true });
        showMessage(response.data.message, 'success');
        this.$router.push('/login');
      } catch (error) {
        console.error(error);
        showMessage('Error logging out!');
      }
    }
  }
};
</script>
  
  <style scoped>
  .homepage {
    min-height: 100vh; /* 使页面占满整个视口高度 */
    background: rgb(85,123,235);
    background: linear-gradient(180deg, rgba(85,123,235,1) 0%, rgba(240,175,122,1) 30%, rgba(217,240,247,0.2576680330335259) 100%);
  }
  
  .main {
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .banner-card {
    width: 100%;
    max-width: 1200px;
    margin-bottom: 30px;
    border-radius: 15px;
    overflow: hidden; /* 确保图片圆角与卡片一致 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加轻微阴影 */
  }
  
  .banner-img {
    width: 100%;
    height: auto;
    display: block;
    object-fit: cover;
  }
  
  .poop-battle {
    text-align: center;
    margin: 15px 0;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    width: 100%;
    max-width: 600px;
  }
  
  .poop-battle h1 {
    margin-bottom: 20px;
    font-size: 26px;
    font-weight: bold;
    color: #333;
  }
  
  .poop-battle .el-button {
    margin: 0 10px;
    font-size: 16px;
  }
  
  .user-card {
  width: 100%;
  max-width: 400px;
  text-align: center;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加轻微阴影 */
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}

.username, .poop-count {
  margin: 10px 0;
  font-size: 18px;
  font-weight: bold;
  color: #555;
}

.logout-button {
  margin-top: 10px;
  font-size: 14px;
}
.oldprojector {
    width: auto; /* 自适应宽度 */
    height: auto; /* 自适应高度 */
    left: 9%; /* 水平居中 */
    top: 72%; /* 垂直居中 */
    position: absolute; 
    transform: scale(0.35); /* 缩小投影机的大小 */
}
</style>
  