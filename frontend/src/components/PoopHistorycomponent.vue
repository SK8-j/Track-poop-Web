<template>  
  <div class="poop-history-page">
    <div class="poop-history">
      <el-table :data="pooplist" style="width: 100%">
        <el-table-column prop="timestamp" label="时间" />
        <el-table-column prop="count" label="记录数量" width="97%" />
      </el-table>
    </div>
  </div> <!-- Added closing div for poop-history-page -->
</template>
  
  <script>
  import axios from 'axios';
import { showMessage } from '../utils/message'; // Assuming you have a message utility for showing messages


    export default {
    name: 'poopHistory',
    data() {
        return {
        pooplist: [],
        updateInterval: null, // 定时器引用
        };
    },
    mounted() {
        this.fetchPoopRecords();
        // 每隔 60 秒自动更新历史数据
        this.updateInterval = setInterval(this.fetchPoopRecords, 60000);
    },
    beforeUnmount() {
        // 清除定时器
        if (this.updateInterval) {
        clearInterval(this.updateInterval);
        }
    },
    methods: {
        async fetchPoopRecords() {
        try {
            const response = await axios.get('http://localhost:5000/poop_history', { withCredentials: true });
            this.pooplist = response.data;
            console.log('Poop Records:', this.pooplist); // Debugging line to check the data
        } catch (error) {
            console.error(error);
            showMessage('Error fetching leaderboard!');
        }
        },
    },
    };
</script>
  
  
  <style scoped>
  .homepage {
  padding: 20px;
  }
  .navbar {
  margin-bottom: 20px;
  }
  .poop-history {
  margin-top: 20px;
  }
  </style>