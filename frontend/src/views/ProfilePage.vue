<template>
  <div class="profile-page">
    <div class="profile-container">
      <el-card class="profile-card" shadow="hover">
        <div class="avatar-container">
          <el-avatar
            :src="user.avatar || 'https://i.postimg.cc/3x3QzSGq/avatar.png'"
            size="large"
          />
        </div>
        <h2 class="username">{{ user.username || '用户名' }}</h2>
        <el-button type="primary" @click="showEditDialog = true">编辑资料</el-button>
        <el-button type="danger" @click="logout">退出登录</el-button>
        <el-button type="info" @click="goToHome">返回主页</el-button> <!-- 添加返回主页按钮 -->
      </el-card>
    </div>


    <!-- 编辑资料的对话框 -->
          <el-dialog
      title="编辑资料"
      v-model="showEditDialog"
      width="30%"
      >
      <el-form :model="editForm">
          <el-form-item label="用户名">
          <el-input v-model="editForm.username"></el-input>
          </el-form-item>
      </el-form>
      <template #footer>
          <el-button @click="showEditDialog = false">取消</el-button>
          <el-button type="primary" @click="updateProfile">保存</el-button>
      </template>
      </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { showMessage } from '../utils/message';
import { useRouter } from 'vue-router'; // 引入路由钩子

export default {
  name: 'ProfilePage',
  data() {
    return {
      user: {
        username: 'poop_master',
        avatar: ''
      },
      editForm: {
      username: '',
      email: ''
    },
    showEditDialog: false
    };
  },
  mounted() {
    this.fetchUserProfile();
  },
  setup() {
    const router = useRouter(); // 获取路由实例
    return {
      router
    };
  },
  methods: {
    async fetchUserProfile() {
      try {
        const response = await axios.get('http://localhost:5000/user_info', {
          withCredentials: true,
        });
        this.user = response.data;
      } catch (error) {
        console.error('Error fetching user info:', error);
        this.$router.push('/login');
      }
    },
    async updateProfile() {
    try {
      const response = await axios.put('http://localhost:5000/update_profile', this.editForm, {
        withCredentials: true,
      });
      showMessage(response.data.message, 'success');
      this.showEditDialog = false;
      this.fetchUserProfile(); // 更新用户资料显示
    } catch (error) {
      console.error('Error updating profile:', error);
      showMessage('更新资料失败，请重试');
    }
  },
    async logout() {
      try {
        await axios.post('http://localhost:5000/logout', {}, { withCredentials: true });
        this.$router.push('/login');
      } catch (error) {
        console.error('Error logging out:', error);
        showMessage('退出登录失败，请重试');
      }
    },
    goToHome() {
      this.router.push('/'); // 导航到主页
    }
  },
};
</script>

<style scoped>
.profile-page {
display: flex;
justify-content: center;
align-items: center;
height: 100vh;
background: rgb(85, 123, 235);
background: linear-gradient(
  180deg,
  rgba(85, 123, 235, 1) 0%,
  rgba(240, 175, 122, 1) 30%,
  rgba(217, 240, 247, 0.2576680330335259) 100%
);
}

.profile-container {
display: flex;
justify-content: center;
align-items: center;
width: 100%;
max-width: 400px;
}

.profile-card {
width: 100%;
padding: 20px;
border-radius: 15px;
background: rgba(255, 255, 255, 0.85);
box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
text-align: center;
}

.avatar-container {
margin-bottom: 20px;
}

.username {
font-size: 24px;
font-weight: bold;
margin-bottom: 10px;
color: #333;
}



.el-button {
margin: 10px 5px;
}
</style>