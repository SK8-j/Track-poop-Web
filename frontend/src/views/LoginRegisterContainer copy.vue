<template>
    <div class="login-register-page">
      <div class="card-container" :class="{ flipped: isFlipped }">
        <div class="login-card">
            <div class="waimiancard">
          <el-card class="form-card" shadow="hover">
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
  
        <div class="register-card">
            <div class="waimiancard">
          <el-card class="form-card" shadow="hover">
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
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { showMessage } from '../utils/message'; // 导入自定义的消息方法
  import { useRouter } from 'vue-router';

  export default {
    name: 'LoginRegisterContainer',
    data() {
      return {
        loginForm: {
          username: '',
          password: ''
        },
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
    mounted() {
      this.checkRoute();
    },
    watch: {
      $route() {
        this.checkRoute();
      }
    },
    methods: {
      async handleLogin() {
      try {
        const response = await axios.post('http://localhost:5000/login', this.loginForm, {
          withCredentials: true,
          // headers: {
          //   'Content-Type': 'application/json'
          // }
        });
        showMessage(response.data.message+'，'+response.data.username, 'success');
        console.log(1);
        this.$router.push('/');
      } catch (error) {
        console.error('Login error:', error);
        if (error.response && error.response.data && error.response.data.message) {
          showMessage(error.response.data.message);
        } else {
          showMessage('登录失败，请检查用户名和密码');
        }
      }
    },
    async handleRegister() {
      try {
        const response = await axios.post('http://localhost:5000/register', this.registerForm, {
          withCredentials: true,
          // headers: {
          //   'Content-Type': 'application/json'
          // }
        });
        showMessage(response.data.message, 'success');
        console.log(1);
        this.$router.push('/login');
      } catch (error) {
        console.error('Register error:', error);
        if (error.response && error.response.data && error.response.data.message) {
          showMessage(error.response.data.message);
        } else {
          showMessage('注册失败，请重试');
        }
      }
    },
      flipToRegister() {
        this.isFlipped = true;
      },
      flipToLogin() {
        this.isFlipped = false;
      },
      checkRoute() {
        if (this.$route.path === '/register') {
          this.isFlipped = true;
        } else {
          this.isFlipped = false;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .login-register-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: rgb(85,123,235);
    background: linear-gradient(135deg, rgba(85,123,235,0.85) 7%, rgba(240,175,122,1) 30%, rgba(217,240,247,0.5259) 80%);
  }
  
  .card-container {
    width: 400px;
    height: 300px;
    position: relative;
    perspective: 1000px;
  }
  
  .login-card,
  .register-card {
    width: 100%;
    height: 100%;
    position: absolute;
    backface-visibility: hidden;
    transition: transform 0.6s ease; /* 将过渡效果应用在卡片上 */

  }
  
  .login-card {
    transform: rotateY(0deg);
  }
  
  .register-card {
    transform: rotateY(180deg);
  }
  
  .flipped .login-card {
    transform: rotateY(-180deg);
  }
  
  .flipped .register-card {
    transform: rotateY(0deg);
  }
  
  .form-card {
    padding: 20px;
    border-radius: 15px;
    background: rgb(85,123,235);
    background: linear-gradient(153deg, rgba(85,123,235,0.8) 0%, rgba(66,207,168,0.5) 67%, rgba(217,240,247,0.7259) 100%);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* 增强阴影效果 */
    width: 80%; /* 确保表单区域有足够的大小 */
    max-width: 350px; /* 限制表单的最大宽度 */
  }
  .form-card h2 {
  font-size: 24px;
  font-weight: bold;
  color: #000000b6; /* 确保标题颜色醒目 */
  /* 使用楷体 */
  font-family: 'KaiTi', sans-serif;
  font-size: 2.34em;
  text-align: center;
  margin-bottom: 20px;
  text-shadow: 0 3px 5px rgb(255, 255, 255); /* 增强阴影效果 */
}
.el-input {
  margin-bottom: 15px;
  
}

.el-button {
  margin-right: 10px;
}

.el-button--primary {
  background-color: #5583eb; /* 提高对比度 */
  border-color: #5583eb;
  color: #fff;
}

.el-button--text {
  color: #345bf5;
  font-weight: bold;
  font-size: 1.34em;
  text-shadow: 0 3px 5px rgb(255, 0, 0); /* 增强阴影效果 */
}

  .waimiancard {
  /* width: 100%;
  height: 100%; */
  padding: 7%;
  border-radius: 15px;
  background-image: url('https://i.postimg.cc/fbG8ZRj6/DALL-E-2024-10-27-00-32-12-A-cute-and-colorful-cartoon-banner-illustration-themed-around-Poop-Bat.webp');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}
  </style>
  