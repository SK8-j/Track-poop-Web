<template>
    <el-header height="60px" class="header">
      <div class="logo">💩💩大作战</div>
      <div class="nav">
        <el-button type="text" @click="goTo('home')">首页</el-button>
        <el-button type="text" @click="goTo('record')">记录💩数</el-button>
        <el-button type="text" @click="goTo('profile')">个人中心</el-button>
      </div>
    </el-header>
  </template>
  
  <script>
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'NavBar',
    setup() {
      const router = useRouter();
      // 跳转函数
      const goTo = (routeName) => {
        if (routeName === 'home') {
          router.push('/');
        } else if (routeName === 'record') {
          router.push('/record');
        } else if (routeName === 'profile') {
          router.push('/profile');
        }
      };
  
      return {
        goTo,
      };
    },
  };
  </script>
  
  <style scoped>
  .header {
    background-color: #2c3e50;
    color: #fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
  }
  
  .logo {
    font-size: 24px;
    font-weight: bold;
  }
  
  .nav .el-button {
    color: #fff;
    margin-left: 20px;
  }
  </style>
  