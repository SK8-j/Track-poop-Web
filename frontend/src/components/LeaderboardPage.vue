<template>
    <div class="leaderboard-page">
      <div class="leaderboard-container">
        <h1>💩排行榜</h1>
        <el-table :data="leaderboardData" stripe>
          <el-table-column prop="username" label="用户名"></el-table-column>
          <el-table-column prop="monthly_poops" label="本月💩数"></el-table-column>
        </el-table>
      </div>
    </div>
</template>

<script>
import axios from 'axios';
import { showMessage } from '../utils/message';

export default {
  name: 'LeaderboardPage',
  data() {
    return {
      leaderboardData: [],
      updateInterval: null, // 定时器引用
    };
  },
  mounted() {
    this.fetchLeaderboard();
    // 每隔 10 秒更新排行榜数据
    this.updateInterval = setInterval(this.fetchLeaderboard, 10000);
  },
  beforeUnmount() {
    // 清除定时器
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
    }
  },
  methods: {
    async fetchLeaderboard() {
      try {
        const response = await axios.get('http://localhost:5000/leaderboard', { withCredentials: true });
        this.leaderboardData = response.data;
      } catch (error) {
        console.error(error);
        showMessage('Error fetching leaderboard!');
      }
    },
  },
};
</script>

<style scoped>
.leaderboard-page {
  min-height: 100vh;
  background: rgb(85, 123, 235);
  background: linear-gradient(180deg, rgba(85, 123, 235, 1) 0%, rgba(240, 175, 122, 1) 30%, rgba(217, 240, 247, 0.2576680330335259) 100%);
}

.leaderboard-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.leaderboard-container h1 {
  margin-bottom: 20px;
  font-size: 26px;
  font-weight: bold;
  color: #333;
}

.el-table {
  width: 100%;
  max-width: 600px;
}
</style>