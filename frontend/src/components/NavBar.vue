<template>
  <div class="navbar">
    <ul class="nav-list">
      <li>
        <router-link :to="`/home/${props.username}/${props.authority}`">首页</router-link>
      </li>
      <li>
        <router-link :to="`/home/${props.username}/${props.authority}/tutorial-generate`">教程生成</router-link>
      </li>
      <li>
        <router-link :to="`/home/${props.username}/${props.authority}/tutorial-execute`">教程执行</router-link>
      </li>
      <li>
        <router-link :to="`/home/${props.username}/${props.authority}/log-management`">日志管理</router-link>
      </li>
      <li>
        <router-link :to="`/home/${props.username}/${props.authority}/guideline-generate`">查看指导书</router-link>
      </li>
      <li>
        <router-link :to="`/home/${props.username}/${props.authority}/weather-entertainment`">天气及娱乐</router-link>
      </li>
    </ul>
    <div class="user-info">
      <span>{{ username }} ({{ authorityText }})</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

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
  width: 250px;
  height: 100%;
  background-color: #2c3e50;
  padding-top: 60px;
  /* 上边栏高度 */
  color: white;
  font-family: Arial, sans-serif;
  box-sizing: border-box;
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
  position: absolute;
  bottom: 20px;
  width: 100%;
  text-align: center;
  color: #ecf0f1;
}
</style>