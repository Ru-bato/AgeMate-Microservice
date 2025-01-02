<template>
  <div class="topbar">
    <div class="logo">
      <router-link to="/home">📚 AgeMate</router-link>
    </div>
    <div class="search-bar">
      <input type="text" placeholder="搜索..." v-model="searchQuery" @keyup.enter="handleSearch" />
      <button @click="handleSearch">🔍</button>
    </div>
    <div class="user-actions">
      <span>{{ username }} ({{ authorityText }})</span>
      <button @click="logout">🔓 退出</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue'
import { useRouter } from 'vue-router'

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

const router = useRouter()

const authorityText = ref(
  props.authority === 1 ? '用户' : '管理员'
)

const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value.trim() } })
    searchQuery.value = ''
  }
}

const logout = () => {
  // 这里添加退出登录的逻辑
  console.log('用户已退出')
  router.push({ name: 'Login' })
}
</script>

<style scoped>
.topbar {
  position: fixed;
  top: 0;
  left: 0px; /* 与侧边栏宽度相同 */
  right: 0;
  height: 60px;
  background-color: #34495e;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.logo a {
  color: white;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
}

.search-bar {
  display: flex;
  align-items: center;
}

.search-bar input {
  padding: 8px 12px;
  border: none;
  border-radius: 4px 0 0 4px;
  outline: none;
  width: 200px;
  font-size: 1rem;
}

.search-bar button {
  padding: 8px 12px;
  border: none;
  background-color: #2ecc71;
  color: white;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 1rem;
}

.search-bar button:hover {
  background-color: #27ae60;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-actions button {
  padding: 8px 12px;
  border: none;
  background-color: #e74c3c;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 1rem;
}

.user-actions button:hover {
  background-color: #c0392b;
}
</style>
