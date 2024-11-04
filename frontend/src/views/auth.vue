<template>
  <div class="login-register-page">
    <div class="card-container" :class="{ flipped: isFlipped }">
      <!-- Login Card -->
      <div class="login-card">
        <div class="waimiancard">
          <el-card class="form-card" shadow="hover">
            <h2>登录</h2>
            <el-form :model="loginForm" @submit.prevent="handleLogin">
              <el-form-item>
                <el-input v-model="loginForm.username" placeholder="用户名"></el-input>
              </el-form-item>
              <el-form-item>
                <el-input type="password" v-model="loginForm.password" placeholder="密码" @keyup.enter="handleLogin"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleLogin">登录</el-button>
                <el-button type="text" @click="flipToRegister">去注册</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </div>

      <!-- Register Card -->
      <div class="register-card">
        <div class="waimiancard">
          <el-card class="form-card" shadow="hover">
            <h2>注册</h2>
            <el-form :model="registerForm" @submit.prevent="handleRegister">
              <el-form-item label="用户名">
                <el-input 
                  v-model="registerForm.username" 
                  clearable 
                  placeholder="请输入用户名" >
                </el-input>
              </el-form-item>
              <el-form-item label="初始💩数量" prop="field105">
                <el-slider :max='30' :step='1' v-model="registerForm.poop_count"></el-slider>
              </el-form-item>
              <el-form-item label="密码">
                <el-input
                  type="password"
                  v-model="registerForm.password"
                  clearable
                  placeholder="请输入密码"
                  show-password
                  @keyup.enter="handleRegister"
                ></el-input>
              </el-form-item>
                
              <!-- Password Strength Indicator -->
              <el-form-item>
                <div class="password-strength">
                  密码强度：<span>{{ passwordStrengthEmoji }}</span>
                  <span style="margin-left: 7%; ">😎/😊/😡?</span>
                </div>
              </el-form-item>
              <el-form-item>
                <el-button 
                  type="primary" 
                  @click="handleRegister" 
                  :disabled="isRegisterDisabled">
                  注册
                </el-button>
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
import { showMessage } from '../utils/message';
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
        password: '',
        poop_count: 0
      },
      isFlipped: true,
      validationStatus: {
        uppercase: false,
        lowercase: false,
        number: false,
        special: false,
        length: false
      },
    };
  },
  computed: {
    // Compute the password strength emoji based on validation status
    passwordStrengthEmoji() {
      const count = Object.values(this.validationStatus).filter(v => v).length;
      if (count >= 5) return '😎'; // Strong
      if (count >= 3) return '😊'; // Medium
      return '😡'; // Weak
    },
    // Determine if the Register button should be disabled
    isRegisterDisabled() {
      // Disable if password strength is Weak
      return this.passwordStrengthEmoji === '😡';
    }
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  mounted() {
    this.checkRoute();
  },
  watch: {
    // Watch for changes in the route to flip cards accordingly
    $route() {
      this.checkRoute();
    },
    // Watch the password field to validate in real-time
    'registerForm.password': function() {
      this.validatePassword();
    }
  },
  methods: {
    // 监听回车事件 点击提交button


    // Validate the password and update validationStatus
    validatePassword() {
      const password = this.registerForm.password;
      this.validationStatus = {
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /\d/.test(password),
        special: /[!@#$%^&*]/.test(password),
        length: password.length >= 8
      };
    },
    // Handle user login
    async handleLogin() {
      try {
        const response = await axios.post('http://localhost:5000/login', this.loginForm, {
          withCredentials: true
        });
        const userId = response.data.user_id; 
        if (userId) {
          showMessage(`${response.data.message}，${response.data.username}`, 'success');
          localStorage.setItem('user_id', userId);
          this.router.push('/');
        } else {
          showMessage('登录失败：未收到用户ID。');
        }
      } catch (error) {
        console.error('登录错误:', error);
        if (error.response && error.response.data && error.response.data.message) {
          showMessage(error.response.data.message);
        } else {
          showMessage('登录失败，请检查用户名和密码');
        }
      }
    },
    // Handle user registration
    async handleRegister() {
      // Ensure password meets at least Medium strength before proceeding
      if (this.isRegisterDisabled) {
        showMessage('密码强度不足，请增强密码后再试。', 'warning');
        return;
      }

      try {
        const response = await axios.post('http://localhost:5000/register', this.registerForm, {
          withCredentials: true
        });
        showMessage(response.data.message, 'success');
        // Automatically log in the user after successful registration
        this.loginForm.username = this.registerForm.username;
        this.loginForm.password = this.registerForm.password;
        await this.handleLogin();
      } catch (error) {
        console.error('注册错误:', error);
        if (error.response && error.response.data && error.response.data.message) {
          showMessage(error.response.data.message);
        } else {
          showMessage('注册失败，请重试');
        }
      }
    },
    // Flip to the Register card
    flipToRegister() {
      this.isFlipped = true;
    },
    // Flip to the Login card
    flipToLogin() {
      this.isFlipped = false;
    },
    // Check the current route to determine if the Register card should be shown
    checkRoute() {
      if (this.$route.query.action === 'register') {
        this.isFlipped = true;
      } else {
        this.isFlipped = false;
      }
    }
  },
};
</script>

<style scoped>
.validation-tooltip {
  position: relative;
  color: red;
  display: inline-block;
  margin-right: 10px;
}
.validation-tooltip::after {
  content: attr(data-tooltip);
  position: absolute;
  background-color: #f9d5d5;
  color: #d9534f;
  padding: 5px;
  border-radius: 4px;
  top: -30px;
  left: 0;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s ease;
}
.validation-tooltip:hover::after {
  opacity: 1;
}

.validation-icons {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
  font-size: 1rem;
}

.password-strength {
  width: 100%;
  font-size: 1.2em;
  color: #ff6347;
  font-weight: bold;
  margin-top: 10px;
  text-align: center;
}

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
  height: 500px;
  position: relative;
  perspective: 1000px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card, .register-card {
  width: 100%;
  height: 100%;
  position: absolute;
  backface-visibility: hidden;
  transition: transform 0.6s ease;
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
  background: linear-gradient(153deg, rgba(85,123,235,0.93) 0%, rgba(66,207,168,0.9) 67%, rgba(217,240,247,0.83) 100%);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  width: 80%;
  max-width: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-card h2 {
  font-size: 24px;
  font-weight: bold;
  color: #000000b6;
  font-family: 'KaiTi', sans-serif;
  font-size: 2.34em;
  text-align: center;
  margin-bottom: 20px;
  text-shadow: 0 3px 5px rgb(255, 255, 255);
}

.el-input {
  margin-bottom: 3%;
}

.el-button {
  margin-right: 10px;
}

.el-button--primary {
  background-color: #5583eb;
  border-color: #5583eb;
  color: #fff;
}

.el-button--text {
  color: #345bf5;
  font-weight: bold;
  font-size: 1.34em;
  text-shadow: 0 3px 5px rgb(255, 0, 0);
}

.waimiancard {
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

.valid {
  color: green;
  display: none;
}

.invalid {
  color: red;
}
</style>
