<template>
  <div class="homepage">
    <!-- 导航栏 -->
    <div class="navbar">
      <NavBar />
    </div>

    <!-- 主要内容区 -->
    <div class="main-wrapper">
      <el-container>
        <el-main class="main-content">
          <!-- 用户信息卡片 -->
          <el-card class="user-info-card" shadow="hover">
            <div class="user-header">
              <el-avatar :size="60" :icon="UserFilled" />
              <div class="user-details">
                <h2>{{ userInfo.username }}</h2>
                <p class="user-stats">总记录: {{ userInfo.poop_count }} 💩</p>
              </div>
              <el-button type="danger" @click="logout" size="small">
                <el-icon><SwitchButton /></el-icon>
                注销
              </el-button>
            </div>
          </el-card>

          <!-- 快速记录区域 -->
          <el-card class="quick-record-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span class="card-title">
                  <el-icon><DocumentAdd /></el-icon>
                  快速记录
                </span>
              </div>
            </template>
            
            <div class="record-buttons">
              <el-button 
                type="primary" 
                size="large" 
                @click="recordPoop(1)"
                :loading="recording"
                class="record-btn"
              >
                <el-icon><Plus /></el-icon>
                记录 1 💩
              </el-button>
              
              <el-button 
                type="success" 
                size="large" 
                @click="recordPoop(2)"
                :loading="recording"
                class="record-btn"
              >
                <el-icon><Plus /></el-icon>
                记录 2 💩
              </el-button>
              
              <el-button 
                type="warning" 
                size="large" 
                @click="showCustomDialog = true"
                :loading="recording"
                class="record-btn"
              >
                <el-icon><Edit /></el-icon>
                自定义
              </el-button>
              
              <el-button 
                type="info" 
                size="large" 
                @click="confirmUndo"
                :loading="recording"
                class="record-btn"
              >
                <el-icon><RefreshLeft /></el-icon>
                撤回
              </el-button>
            </div>
          </el-card>

          <!-- 今日统计快览 -->
          <el-card class="today-stats-card" shadow="hover">
            <template #header>
              <span class="card-title">
                <el-icon><Calendar /></el-icon>
                今日统计
              </span>
            </template>
            
            <div class="today-stats">
              <div class="stat-item">
                <div class="stat-number">{{ todayStats.total_count || 0 }}</div>
                <div class="stat-label">今日总数</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ todayStats.record_count || 0 }}</div>
                <div class="stat-label">记录次数</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ recentAverage }}</div>
                <div class="stat-label">近期日均</div>
              </div>
            </div>
          </el-card>

          <!-- 每日概览 -->
          <DailyDashboard />
        </el-main>

        <!-- 侧边栏：排行榜 -->
        <el-aside class="sidebar" width="300px">
          <div class="leaderboard-container">
            <LeaderboardPage />
          </div>
        </el-aside>
      </el-container>
    </div>

    <!-- 自定义记录对话框 -->
    <el-dialog
      v-model="showCustomDialog"
      title="自定义记录"
      width="400px"
      center
    >
      <el-form @submit.prevent="recordCustomPoop">
        <el-form-item label="记录数量:">
          <el-input-number
            v-model="customCount"
            :min="0"
            :max="10"
            size="large"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        <el-alert
          title="提示"
          description="为了数据准确性，系统会对异常记录进行检测"
          type="info"
          :closable="false"
          show-icon
        />
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCustomDialog = false">取消</el-button>
          <el-button type="primary" @click="recordCustomPoop" :loading="recording">
            确认记录
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { UserFilled, SwitchButton, DocumentAdd, Plus, Edit, RefreshLeft, Calendar } from '@element-plus/icons-vue'
import NavBar from '../components/NavBar.vue'
import LeaderboardPage from '@/components/LeaderboardPage.vue'
import DailyDashboard from '@/components/DailyDashboard.vue'
import axios from 'axios'
import { showMessage } from '../utils/message'

export default {
  name: 'HomePage',
  components: {
    NavBar,
    LeaderboardPage,
    DailyDashboard,
    UserFilled,
    SwitchButton,
    DocumentAdd,
    Plus,
    Edit,
    RefreshLeft,
    Calendar
  },
  data() {
    return {
      userInfo: {
        username: 'Loading...',
        poop_count: 0
      },
      todayStats: {
        total_count: 0,
        record_count: 0
      },
      recentAverage: 0,
      recording: false,
      showCustomDialog: false,
      customCount: 1
    }
  },
  mounted() {
    this.fetchUserInfo()
    this.fetchTodayStats()
  },
  methods: {
    async fetchUserInfo() {
      try {
        const response = await axios.get('http://localhost:5000/user_info', { 
          withCredentials: true 
        })
        this.userInfo = response.data
      } catch (error) {
        console.error('Error fetching user info:', error)
        showMessage('无法加载用户信息，请重新登录', 'error')
        this.$router.push('/login')
      }
    },

    async fetchTodayStats() {
      try {
        const today = new Date().toISOString().split('T')[0]
        const response = await axios.get('http://localhost:5000/daily_stats', {
          params: {
            start_date: today,
            end_date: today
          },
          withCredentials: true
        })
        
        const dailyStats = response.data.daily_stats
        if (dailyStats.length > 0) {
          this.todayStats = dailyStats[0]
        }

        // 计算近期平均值
        const weekAgo = new Date()
        weekAgo.setDate(weekAgo.getDate() - 7)
        const weekResponse = await axios.get('http://localhost:5000/daily_stats', {
          params: {
            start_date: weekAgo.toISOString().split('T')[0],
            end_date: today
          },
          withCredentials: true
        })
        
        const weekStats = weekResponse.data.daily_stats
        const totalCount = weekStats.reduce((sum, stat) => sum + stat.total_count, 0)
        this.recentAverage = (totalCount / 7).toFixed(1)
        
      } catch (error) {
        console.error('Error fetching today stats:', error)
      }
    },

    async recordPoop(count) {
      this.recording = true
      try {
        const response = await axios.post('http://localhost:5000/record_poop', {
          poop_count: count
        }, { withCredentials: true })
        
        showMessage(response.data.message, 'success')
        
        // 刷新数据
        await Promise.all([
          this.fetchUserInfo(),
          this.fetchTodayStats()
        ])
        
        // 通知父组件刷新
        this.$emit('dataUpdated')
        
      } catch (error) {
        console.error('Recording error:', error)
        const message = error.response?.data?.message || '记录失败'
        const isAnomalous = error.response?.data?.is_suspicious
        
        showMessage(message, isAnomalous ? 'warning' : 'error')
        
        if (isAnomalous) {
          this.$notify({
            title: '异常检测',
            message: '系统检测到异常记录模式，请确保数据准确性',
            type: 'warning',
            duration: 5000
          })
        }
      } finally {
        this.recording = false
      }
    },

    async recordCustomPoop() {
      if (this.customCount < 0 || this.customCount > 10) {
        showMessage('记录数量应在0-10之间', 'warning')
        return
      }
      
      await this.recordPoop(this.customCount)
      this.showCustomDialog = false
      this.customCount = 1
    },

    async logout() {
      try {
        const response = await axios.post('http://localhost:5000/logout', {}, { 
          withCredentials: true 
        })
        showMessage(response.data.message, 'success')
        this.$router.push('/login')
      } catch (error) {
        console.error(error)
        showMessage('注销失败', 'error')
      }
    },

    confirmUndo() {
      this.$confirm(
        '确定要撤回今天的最后一次记录吗？',
        '撤回确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      ).then(() => {
        this.recordPoop(-1)
      }).catch(() => {
        // 用户取消
      })
    }
  }
}
</script>

<style scoped>
.homepage {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.navbar {
  height: 60px;
  background-color: rgba(44, 62, 80, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.main-wrapper {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.main-content {
  padding: 0 20px;
}

.user-info-card {
  margin-bottom: 20px;
  border-radius: 12px;
  border: none;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.user-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 10px 0;
}

.user-details {
  flex: 1;
}

.user-details h2 {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 24px;
}

.user-stats {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.quick-record-card,
.today-stats-card {
  margin-bottom: 20px;
  border-radius: 12px;
  border: none;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.record-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  padding: 10px 0;
}

.record-btn {
  height: 60px;
  font-size: 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.record-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.today-stats {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.sidebar {
  padding-left: 20px;
}

.leaderboard-container {
  position: sticky;
  top: 20px;
}

/* 移动端适配 */
@media (max-width: 1200px) {
  .sidebar {
    display: none;
  }
  
  .main-content {
    padding: 0 10px;
  }
}

@media (max-width: 768px) {
  .main-wrapper {
    padding: 10px;
  }
  
  .user-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
  
  .record-buttons {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .record-btn {
    height: 50px;
    font-size: 14px;
  }
  
  .today-stats {
    flex-direction: column;
    gap: 20px;
  }
  
  .stat-number {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .record-buttons {
    grid-template-columns: 1fr;
  }
  
  .user-details h2 {
    font-size: 20px;
  }
  
  .user-stats {
    font-size: 14px;
  }
}

/* 对话框样式 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* 动画效果 */
.el-card {
  transition: all 0.3s ease;
}

.el-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}
</style>

<script>
import { UserFilled, SwitchButton, DocumentAdd, Plus, Edit, RefreshLeft, Calendar } from '@element-plus/icons-vue'
import NavBar from '../components/NavBar.vue'
import LeaderboardPage from '@/components/LeaderboardPage.vue'
import DailyDashboard from '@/components/DailyDashboard.vue'
import axios from 'axios'
import { showMessage } from '../utils/message'

export default {
  name: 'HomePage',
  components: {
    NavBar,
    LeaderboardPage,
    DailyDashboard,
    UserFilled,
    SwitchButton,
    DocumentAdd,
    Plus,
    Edit,
    RefreshLeft,
    Calendar
  },
  data() {
    return {
      userInfo: {
        username: 'Loading...',
        poop_count: 0
      },
      todayStats: {
        total_count: 0,
        record_count: 0
      },
      recentAverage: 0,
      recording: false,
      showCustomDialog: false,
      customCount: 1
    }
  },
  mounted() {
    this.fetchUserInfo()
    this.fetchTodayStats()
  },
  methods: {
    async fetchUserInfo() {
      try {
        const response = await axios.get('http://localhost:5000/user_info', { 
          withCredentials: true 
        })
        this.userInfo = response.data
      } catch (error) {
        console.error('Error fetching user info:', error)
        showMessage('无法加载用户信息，请重新登录', 'error')
        this.$router.push('/login')
      }
    },

    async fetchTodayStats() {
      try {
        const today = new Date().toISOString().split('T')[0]
        const response = await axios.get('http://localhost:5000/daily_stats', {
          params: {
            start_date: today,
            end_date: today
          },
          withCredentials: true
        })
        
        const dailyStats = response.data.daily_stats
        if (dailyStats.length > 0) {
          this.todayStats = dailyStats[0]
        }

        // 计算近期平均值
        const weekAgo = new Date()
        weekAgo.setDate(weekAgo.getDate() - 7)
        const weekResponse = await axios.get('http://localhost:5000/daily_stats', {
          params: {
            start_date: weekAgo.toISOString().split('T')[0],
            end_date: today
          },
          withCredentials: true
        })
        
        const weekStats = weekResponse.data.daily_stats
        const totalCount = weekStats.reduce((sum, stat) => sum + stat.total_count, 0)
        this.recentAverage = (totalCount / 7).toFixed(1)
        
      } catch (error) {
        console.error('Error fetching today stats:', error)
      }
    },

    async recordPoop(count) {
      this.recording = true
      try {
        const response = await axios.post('http://localhost:5000/record_poop', {
          poop_count: count
        }, { withCredentials: true })
        
        showMessage(response.data.message, 'success')
        
        // 刷新数据
        await Promise.all([
          this.fetchUserInfo(),
          this.fetchTodayStats()
        ])
        
        // 通知父组件刷新
        this.$emit('dataUpdated')
        
      } catch (error) {
        console.error('Recording error:', error)
        const message = error.response?.data?.message || '记录失败'
        const isAnomalous = error.response?.data?.is_suspicious
        
        showMessage(message, isAnomalous ? 'warning' : 'error')
        
        if (isAnomalous) {
          this.$notify({
            title: '异常检测',
            message: '系统检测到异常记录模式，请确保数据准确性',
            type: 'warning',
            duration: 5000
          })
        }
      } finally {
        this.recording = false
      }
    },

    async recordCustomPoop() {
      if (this.customCount < 0 || this.customCount > 10) {
        showMessage('记录数量应在0-10之间', 'warning')
        return
      }
      
      await this.recordPoop(this.customCount)
      this.showCustomDialog = false
      this.customCount = 1
    },

    async logout() {
      try {
        const response = await axios.post('http://localhost:5000/logout', {}, { 
          withCredentials: true 
        })
        showMessage(response.data.message, 'success')
        this.$router.push('/login')
      } catch (error) {
        console.error(error)
        showMessage('注销失败', 'error')
      }
    },

    confirmUndo() {
      this.$confirm(
        '确定要撤回今天的最后一次记录吗？',
        '撤回确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      ).then(() => {
        this.recordPoop(-1)
      }).catch(() => {
        // 用户取消
      })
    }
  }
}
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
  position: fixed;
  top: 20px;
  right: 20px;
  width: 300px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

@media (max-width: 768px) {
  .leaderboard-fixed {
    position: static;
    width: 100%;
    margin-top: 20px;
    right: 0;
    top: 0;
  }
}

/* 媒体查询，当屏幕宽度小于 768px 时应用以下样式（适用于大多数移动设备） */
@media (max-width: 768px) {
 .main-content-wrap {
    flex-direction: column;
  }

 .main-content {
    width: 100%;
  }
}
</style>