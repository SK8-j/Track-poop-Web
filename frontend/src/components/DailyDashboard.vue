<template>
  <div class="daily-dashboard">
    <el-card class="dashboard-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="dashboard-title">
            <el-icon><Calendar /></el-icon>
            每日记录概览
          </span>
          <el-date-picker
            v-model="selectedMonth"
            type="month"
            placeholder="选择月份"
            size="small"
            @change="fetchMonthlyData"
          />
        </div>
      </template>

      <div class="dashboard-content">
        <!-- 月度统计卡片 -->
        <div class="stats-grid">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-item">
              <div class="stat-value">{{ monthlyOverview.total_poops }}</div>
              <div class="stat-label">本月总数</div>
            </div>
          </el-card>
          
          <el-card class="stat-card" shadow="hover">
            <div class="stat-item">
              <div class="stat-value">{{ monthlyOverview.days_recorded }}</div>
              <div class="stat-label">记录天数</div>
            </div>
          </el-card>
          
          <el-card class="stat-card" shadow="hover">
            <div class="stat-item">
              <div class="stat-value">{{ monthlyOverview.average_per_day }}</div>
              <div class="stat-label">日均记录</div>
            </div>
          </el-card>
          
          <el-card class="stat-card" shadow="hover">
            <div class="stat-item">
              <div class="stat-value">{{ todayCount }}</div>
              <div class="stat-label">今日记录</div>
            </div>
          </el-card>
        </div>

        <!-- 日历视图 -->
        <div class="calendar-section">
          <h3>月度日历</h3>
          <el-calendar v-model="selectedDate" class="custom-calendar">
            <template #date-cell="{ data }">
              <div class="calendar-day" :class="getDayClass(data.day)">
                <div class="day-number">{{ data.day.split('-').pop() }}</div>
                <div class="day-count" v-if="getDayCount(data.day) > 0">
                  💩 {{ getDayCount(data.day) }}
                </div>
              </div>
            </template>
          </el-calendar>
        </div>

        <!-- 最近记录列表 -->
        <div class="recent-records">
          <h3>最近记录</h3>
          <el-timeline>
            <el-timeline-item
              v-for="record in recentRecords"
              :key="record.timestamp"
              :timestamp="formatTimestamp(record.timestamp)"
              placement="top"
            >
              <div class="record-item">
                <el-tag :type="getRecordType(record.count)" size="small">
                  {{ record.count }} 💩
                </el-tag>
              </div>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { Calendar } from '@element-plus/icons-vue'
import axios from 'axios'
import { showMessage } from '../utils/message'

export default {
  name: 'DailyDashboard',
  components: {
    Calendar
  },
  data() {
    return {
      selectedDate: new Date(),
      selectedMonth: new Date(),
      dailyStats: [],
      monthlyOverview: {
        total_poops: 0,
        days_recorded: 0,
        average_per_day: 0,
        total_records: 0
      },
      recentRecords: [],
      loading: false
    }
  },
  computed: {
    todayCount() {
      const today = new Date().toISOString().split('T')[0]
      const todayStat = this.dailyStats.find(stat => stat.date === today)
      return todayStat ? todayStat.total_count : 0
    }
  },
  mounted() {
    this.fetchDashboardData()
  },
  methods: {
    async fetchDashboardData() {
      this.loading = true
      try {
        await Promise.all([
          this.fetchDailyStats(),
          this.fetchMonthlyData(),
          this.fetchRecentRecords()
        ])
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
        showMessage('加载数据失败', 'error')
      } finally {
        this.loading = false
      }
    },

    async fetchDailyStats() {
      try {
        const endDate = new Date()
        const startDate = new Date()
        startDate.setDate(startDate.getDate() - 30)

        const response = await axios.get('http://localhost:5000/daily_stats', {
          params: {
            start_date: startDate.toISOString().split('T')[0],
            end_date: endDate.toISOString().split('T')[0]
          },
          withCredentials: true
        })
        
        this.dailyStats = response.data.daily_stats
      } catch (error) {
        console.error('Error fetching daily stats:', error)
        throw error
      }
    },

    async fetchMonthlyData() {
      try {
        const year = this.selectedMonth.getFullYear()
        const month = this.selectedMonth.getMonth() + 1

        const response = await axios.get('http://localhost:5000/monthly_overview', {
          params: { year, month },
          withCredentials: true
        })
        
        this.monthlyOverview = response.data
      } catch (error) {
        console.error('Error fetching monthly data:', error)
        throw error
      }
    },

    async fetchRecentRecords() {
      try {
        const response = await axios.get('http://localhost:5000/poop_history', {
          withCredentials: true
        })
        
        this.recentRecords = response.data.slice(0, 10) // 最近10条记录
      } catch (error) {
        console.error('Error fetching recent records:', error)
        throw error
      }
    },

    getDayCount(dateStr) {
      const stat = this.dailyStats.find(s => s.date === dateStr)
      return stat ? stat.total_count : 0
    },

    getDayClass(dateStr) {
      const count = this.getDayCount(dateStr)
      if (count === 0) return 'day-empty'
      if (count <= 2) return 'day-normal'
      if (count <= 4) return 'day-high'
      return 'day-extreme'
    },

    getRecordType(count) {
      if (count === 0) return 'info'
      if (count === 1) return 'success'
      if (count === 2) return 'warning'
      return 'danger'
    },

    formatTimestamp(timestamp) {
      return new Date(timestamp).toLocaleString('zh-CN')
    }
  }
}
</script>

<style scoped>
.daily-dashboard {
  padding: 20px;
}

.dashboard-card {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  text-align: center;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-item {
  padding: 20px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.calendar-section h3,
.recent-records h3 {
  margin-bottom: 20px;
  color: #333;
  font-size: 16px;
}

.custom-calendar {
  max-width: 100%;
}

.calendar-day {
  padding: 5px;
  min-height: 60px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.day-number {
  font-weight: bold;
  margin-bottom: 4px;
}

.day-count {
  font-size: 12px;
  color: #666;
}

.day-empty {
  background-color: #f8f9fa;
}

.day-normal {
  background-color: #e3f2fd;
  border-left: 3px solid #2196f3;
}

.day-high {
  background-color: #fff3e0;
  border-left: 3px solid #ff9800;
}

.day-extreme {
  background-color: #ffebee;
  border-left: 3px solid #f44336;
}

.record-item {
  display: flex;
  align-items: center;
}

.recent-records {
  max-height: 400px;
  overflow-y: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .daily-dashboard {
    padding: 10px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .stat-value {
    font-size: 24px;
  }
  
  .calendar-section,
  .recent-records {
    margin-top: 20px;
  }
}
</style>