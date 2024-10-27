<template>
    <div class="login-page">
      <div class="card-container" :class="{ flipped: isFlipped }">
        <el-card class="login-card" shadow="hover">
          <h2>登录</h2>
          <el-form :model="loginForm" @submit.prevent="handleLogin">
            <el-form-item>
              <el-input v-model="loginForm.username" placeholder="用户名"></el-input>
            </el-form-item>
            <el-form-item>
              <el-input type="password" v-model="loginForm.password" placeholder="密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleLogin">登录</el-button>
              <el-button type="text" @click="flipToRegister">去注册</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import { showMessage } from '../utils/message';
  
  export default {
    name: 'LoginPage', // 使用多词名称
    data() {
      return {
        loginForm: {
          username: '',
          password: ''
        },
        isFlipped: false
      };
    },
    setup() {
      const router = useRouter();
      return { router };
    },
    methods: {
      async handleLogin() {
        try {
          const response = await axios.post('http://localhost:5000/login', this.loginForm, { withCredentials: true });
          const userId = response.data.user_id; 
          if (userId) {
              localStorage.setItem('user_id', userId); // 将用户ID存储到localStorage中
              showMessage(response.data.message);
          // 登录成功后跳转到首页
            this.$router.push('/');
        } else {
            showMessage('Login failed: user ID not received.');
            }
        } catch (error) {
            showMessage('Invalid credentials');
        }
      },
      flipToRegister() {
      this.isFlipped = true;
      setTimeout(() => {
        this.$router.push('/register');
        this.isFlipped = false;
      }, 500);
      }
    }
  };
  </script>
  
  <style scoped>
  .login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f7fa; /* 和homepage背景一致 */
  }
  
  .card-container {
    perspective: 1000px;
  }
  
  .login-card {
    width: 400px;
    padding: 20px;
    border-radius: 15px;
    transform-style: preserve-3d;
    transition: transform 0.5s, opacity 0.25s;
  }
  
  .flipped .login-card {
    transform: rotateY(130deg);
    transition: transform 0.5s, opacity 0.25s;
  }
  </style>
  