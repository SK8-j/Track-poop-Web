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
                <el-input
                  type="password"
                  v-model="registerForm.password"
                  placeholder="密码"
                  @input="validatePassword"
                  suffix-icon="passwordValidationIcon"
                ></el-input>
              </el-form-item>
              <el-form-item>
                <div class="validation-icons">
                  <span :class="validationIconClass.uppercase">包含大写字母</span>
                  <span :class="validationIconClass.lowercase">包含小写字母</span>
                  <span :class="validationIconClass.number">包含数字</span>
                  <span :class="validationIconClass.special">包含特殊字符</span>
                  <span :class="validationIconClass.length">至少8位</span>
                </div>
              </el-form-item>
              <el-form-item>
                <div class="password-strength">
                  密码强度：<span>{{ passwordStrengthEmoji }}</span>
                </div>
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
        password: ''
      },
      isFlipped: false,
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
    passwordValidationIcon() {
      return this.isPasswordValid ? 'el-icon-check' : 'el-icon-close';
    },
    isPasswordValid() {
      return this.validationStatus.uppercase && this.validationStatus.lowercase &&
             this.validationStatus.number && this.validationStatus.special &&
             this.validationStatus.length;
    },
    validationIconClass() {
      return {
        uppercase: this.validationStatus.uppercase ? 'valid' : 'invalid',
        lowercase: this.validationStatus.lowercase ? 'valid' : 'invalid',
        number: this.validationStatus.number ? 'valid' : 'invalid',
        special: this.validationStatus.special ? 'valid' : 'invalid',
        length: this.validationStatus.length ? 'valid' : 'invalid',
      };
    },
    passwordStrength() {
      let strength = Object.values(this.validationStatus).filter(Boolean).length;
      return strength;
    },
    passwordStrengthEmoji() {
      return '💩'.repeat(this.passwordStrength);
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
    $route() {
      this.checkRoute();
    }
  },
  methods: {
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
    async handleLogin() {
      try {
        const response = await axios.post('http://localhost:5000/login', this.loginForm, {
          withCredentials: true
        });
        const userId = response.data.user_id; 
        if (userId) {
          showMessage(response.data.message + '，' + response.data.username, 'success');
          localStorage.setItem('user_id', userId);
          this.router.push('/home');
        } else {
          showMessage('Login failed: user ID not received.');
        }
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
          withCredentials: true
        });
        showMessage(response.data.message, 'success');
        this.loginForm.username = this.registerForm.username;
        this.loginForm.password = this.registerForm.password;
        await this.handleLogin();
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
      if (this.$route.path === '/auth' && this.$route.query.action === 'register') {
        this.isFlipped = true;
      } else {
        this.isFlipped = false;
      }
    }
  },

};
</script>

<style scoped>
 
  
  .valid {
    color: green;
  }
  
  .invalid {
    color: red;
  }

/* 验证图标和文字 */
.validation-icons {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
  font-size: 1rem;
}

.password-strength {
  font-size: 1.2em;
  color: #ff6347;
  font-weight: bold;
  margin-top: 10px;
  text-align: center;
}
  /* 外部容器，确保整个页面居中 */
.login-register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: rgb(85,123,235);
  background: linear-gradient(135deg, rgba(85,123,235,0.85) 7%, rgba(240,175,122,1) 30%, rgba(217,240,247,0.5259) 80%);
}
  
  /* 卡片容器 */
.card-container {
  width: 400px;
  height: auto;
  position: relative;
  perspective: 1000px;
  display: flex;
  justify-content: center;
  align-items: center;
}
  
  .login-card{
    width: 100%;
    height: 100%;
    position: absolute;
    backface-visibility: hidden;
    transition: transform 0.6s ease; /* 将过渡效果应用在卡片上 */

  }
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
  
  /* 表单卡片样式 */
.form-card {
  padding: 20px;
  border-radius: 15px;
  background: rgb(85,123,235);
  background: linear-gradient(153deg, rgba(85,123,235,0.8) 0%, rgba(66,207,168,0.5) 67%, rgba(217,240,247,0.7259) 100%);
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
  
