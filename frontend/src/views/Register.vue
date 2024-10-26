<template>
    <div class="register-page">
      <div class="card-container" :class="{ flipped: isFlipped }">
        <el-card class="register-card" shadow="hover">
          <h2>注册</h2>
          <el-form :model="registerForm" @submit.prevent="handleRegister">
            <el-form-item>
              <el-input v-model="registerForm.username" placeholder="用户名"></el-input>
            </el-form-item>
            <el-form-item>
              <el-input type="password" v-model="registerForm.password" placeholder="密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleRegister">注册</el-button>
              <el-button type="text" @click="flipToLogin">已有账号？登录</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'RegisterPage', // 修改为多词名称
    data() {
      return {
        registerForm: {
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
      async handleRegister() {
        try {
          const response = await axios.post('http://localhost:5000/register', this.registerForm);
          alert(response.data.message);
          this.router.push('/login');
        } catch (error) {
          alert('注册失败，请重试!');
        }
      },
      flipToLogin() {
      this.isFlipped = true;
      setTimeout(() => {
        this.$router.push('/login');
        this.isFlipped = false;
      }, 500);
     }
    }
  };
  </script>
  
  <style scoped>
  .register-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f7fa; /* 和homepage背景一致 */
  }
  
  .card-container {
    perspective: 1000px;
  }
  
  .register-card {
    width: 400px;
    padding: 20px;
    border-radius: 15px;
    transform-style: preserve-3d;
  }
  
  .flipped .register-card {
    transform: rotateY(130deg);
    transition: transform 0.5s, opacity 0.25s;
  }
  </style>
  