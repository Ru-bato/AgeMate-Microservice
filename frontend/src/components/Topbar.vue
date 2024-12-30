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

  <!-- 悬浮搜索结果列表 -->
  <el-dialog v-model="isDialogVisible" title="搜索结果" width="50%" @close="handleClose">
    <div v-if="searchResults.length > 0">
      <el-card class="card" v-for="(log, index) in searchResults" :key="index" style="margin: 10px;">
        <div class="card-header">
          <h2>{{ log.title }}</h2>
        </div>
        <div class="card-footer">
          <el-button type="primary" @click="openMarkdownDialog(log)">点击查看</el-button>
        </div>
      </el-card>
    </div>
    <div v-else>
      <p>没有找到相关日志。</p>
    </div>
  </el-dialog>

  <!-- 使用 ElDialog 显示 Markdown 内容 -->
  <el-dialog v-model="dialogVisible" title="日志内容" width="70%" @close="handleClose">
    <div v-html="markdownContent" class="markdown-content"></div>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="addFavorite(currentLog)">收藏</el-button>
        <el-button type="danger" @click="deleteLog(currentLog.log_id)">删除</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElNotification } from 'element-plus'
import { marked } from 'marked'

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

const authorityText = ref(props.authority === 1 ? '管理员' : '普通用户')

const searchQuery = ref('')
const isDialogVisible = ref(false) // 控制悬浮窗显示
const searchResults = ref<Array<{ log_id: string, title: string, content: string }>>([]) // 存储搜索结果
const dialogVisible = ref(false) // 控制日志内容弹窗显示
const markdownContent = ref('') // 存储 Markdown 内容
const currentLog = ref<{ log_id: string, title: string, content: string } | null>(null) // 当前查看的日志

// 搜索功能
const handleSearch = async () => {
  if (searchQuery.value.trim()) {
    try {
      const response = await axios.get("http://127.0.0.1:8000/logs/search", {
        params: { user_id: 1, keyword: searchQuery.value.trim() }
      })
      searchResults.value = response.data
      isDialogVisible.value = true // 显示搜索结果的悬浮窗
      searchQuery.value = '' // 清空搜索框
    } catch (error) {
      console.error('搜索失败:', error)
      errorInfo("搜索失败，请重试！")
    }
  }
}

// 打开 Markdown 日志内容
const openMarkdownDialog = (log: { log_id: string, content: string }) => {
  markdownContent.value = marked(log.content) // 将 Markdown 转换为 HTML
  currentLog.value = log // 保存当前日志
  dialogVisible.value = true // 打开查看日志的弹窗
}

// 收藏日志
const addFavorite = async (log: { log_id: string }) => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/logs/favorites/", null, {
      params: { user_id: 1, log_id: log.log_id }
    })
    successInfo("收藏成功！")
  } catch (error) {
    console.error('收藏失败:', error)
    errorInfo("收藏失败，已收藏或网络原因！")
  }
}

// 删除日志
const deleteLog = async (log_id: string) => {
  try {
    const response = await axios.delete(`http://127.0.0.1:8000/logs/${log_id}`, {
      params: { user_id: 1 }
    })
    successInfo("日志删除成功！")
    await getSearchResults() // 重新加载搜索结果
  } catch (error) {
    console.error('删除日志失败:', error)
    errorInfo("删除日志失败，请重试！")
  }
}

// 成功通知函数
const successInfo = (message: string) => {
  ElNotification({
    title: 'Success',
    message: message,
    type: 'success',
  })
}

// 错误通知函数
const errorInfo = (message: string) => {
  ElNotification({
    title: 'Error',
    message: message,
    type: 'error',
  })
}

// 关闭弹窗时清空内容
const handleClose = () => {
  markdownContent.value = ''
  currentLog.value = null
}
</script>

<style scoped>
.topbar {
  position: fixed;
  top: 0;
  left: 0;
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
}

.search-bar button {
  padding: 8px 12px;
  border: none;
  background-color: #2ecc71;
  color: white;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  transition: background-color 0.3s;
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
}

.user-actions button:hover {
  background-color: #c0392b;
}

.card {
  margin: 10px;
}

.card-header {
  font-size: 1.2rem;
  font-weight: bold;
}

.card-footer {
  text-align: right;
}

.el-button {
  font-size: 1rem;
  margin-left: 10px;
}
</style>
