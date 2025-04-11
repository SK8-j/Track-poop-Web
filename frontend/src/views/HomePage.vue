<template>
  <div class="homepage">
    <div class="navbar">
      <NavBar />
    </div>
    <!-- 图片大屏及其他内容 -->
    <div class="main-content-wrap">
      <el-main class="main-content">
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

        <!-- 用户信息区域 -->
        <el-card class="user-card" shadow="hover">
          <div class="user-info">
            <el-avatar size="large" src="your-avatar-image-url" />
            <p class="username">用户名: {{ userInfo.username }}</p>
            <p class="poop-count">💩数: {{ userInfo.poop_count }}</p>
            <el-button type="danger" @click="logout" class="logout-button">注销</el-button>
          </div>
        </el-card>
        <el-button type="info" @click="showLeaderboard">查看排行榜</el-button>
      </el-main>

      <!-- 排行榜区域 -->
      <div class="leaderboard-fixed">
        <LeaderboardPage />
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import axios from 'axios';
import { showMessage } from '../utils/message';
import LeaderboardPage from '@/components/LeaderboardPage.vue';

export default {
  name: 'HomePage',
  components: {
    NavBar,
    LeaderboardPage
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
        showMessage(error.response.data.message);
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
    },
    async showLeaderboard() {
      try {
        const response = await axios.get('http://localhost:5000/leaderboard', { withCredentials: true });
        const leaderboardData = response.data;
        // 可以在这里显示排行榜数据，例如使用弹窗
        alert(JSON.stringify(leaderboardData, null, 2));
      } catch (error) {
        console.error(error);
        showMessage('Error fetching leaderboard!');
      }
    }
  }
};
</script>

<style scoped>
.homepage {
  min-height: 100vh;
  background: rgb(85, 123, 235);
  background: linear-gradient(180deg, rgba(85, 123, 235, 1) 0%, rgba(240, 175, 122, 1) 30%, rgba(217, 240, 247, 0.2576680330335259) 100%);
  display: flex;
  flex-direction: column;
}

.navbar {
  width: 100%;
  height: 60px; /* 设置导航栏高度 */
  background-color: #2c3e50; /* 导航栏背景颜色 */
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.main-content-wrap {
  display: flex;
  flex-direction: column; /* 在小屏幕上改为垂直排列 */
  flex: 1;
  padding: 0 10px; /* 增加内边距以优化小屏幕显示 */
}

.main-content {
  width: 100%;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.banner-card {
  width: 100%;
  max-width: 100%; /* 使卡片在小屏幕上占满宽度 */
  margin-bottom: 30px;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
  max-width: 100%; /* 使按钮区域在小屏幕上占满宽度 */
}

.poop-battle h1 {
  margin-bottom: 20px;
  font-size: 22px; /* 减小标题字体大小 */
  font-weight: bold;
  color: #333;
}

.poop-battle.el-button {
  margin: 0 5px; /* 减小按钮间距 */
  font-size: 14px; /* 减小按钮字体大小 */
}

.user-card {
  width: 100%;
  max-width: 100%; /* 使卡片在小屏幕上占满宽度 */
  text-align: center;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}

.username,
.poop-count {
  margin: 10px 0;
  font-size: 16px; /* 减小用户名和排便数的字体大小 */
  font-weight: bold;
  color: #555;
}

.logout-button {
  margin-top: 10px;
  font-size: 14px;
}

.leaderboard-fixed {
  width: 100%;
  margin-top: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 媒体查询，当屏幕宽度小于 768px 时应用以下样式（适用于大多数移动设备） */
@media (max-width: 768px) {
 .main-content-wrap {
    flex-direction: column;
  }

 .main-content {
    width: 100%;
  }

 .leaderboard-fixed {
    width: 100%;
    position: relative;
    top: 0;
    right: 0;
  }
}
</style>