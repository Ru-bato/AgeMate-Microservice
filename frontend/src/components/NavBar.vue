<template>
  <div class="navbar">
    <ul class="nav-list">
      <li><router-link to="/home">首页</router-link></li>
      <li><router-link to="/home/tutorial-generate">教程生成</router-link></li>
      <li><router-link to="/home/tutorial-execute">教程执行</router-link></li>
      <li><router-link to="/home/log-management">日志管理</router-link></li>
      <li><router-link to="/home/guideline-generate">查看指导书</router-link></li>
      <li><router-link to="/home/my-favourites">我的指导书收藏</router-link></li>
      <!-- <li><router-link to="/home/weather-entertainment">天气及娱乐</router-link></li> -->
    </ul>
    <div class="user-info">
      <!-- <span>{{ username }} ({{ authorityText }})</span> -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue'

const props = defineProps({
  username: {
    type: String,
    required: true,
  },
  authority: {
    type: Number,
    required: true,
  },
})

const authorityText = ref(
  props.authority === 1 ? '管理员' : '普通用户'
)
</script>

<style scoped>
.navbar {
  position: fixed;
  /* top: 0;
  left: 0; */
  left: 0;
  top: 30px;
  width: 250px;
  height: 100%;
  background-color: #2c3e50;
  padding-top: 80px;
  /* 上边栏高度 */
  color: white;
  font-family: Arial, sans-serif;
}

.nav-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.nav-list li {
  padding: 15px 20px;
  text-align: center;
}

.nav-list li a {
  color: white;
  text-decoration: none;
  display: block;
}

.nav-list li a:hover {
  background-color: #34495e;
}

.user-info {
  position: fixed;
  bottom: 20px;
  width: 250px;
  text-align: center;
  color: #ecf0f1;
}
</style>
