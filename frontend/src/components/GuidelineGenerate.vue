<template>
  <div class="home-page">
    <div class="welcome-message">
      <!-- 循环展示所有日志 -->
      <el-card
        class="card"
        v-for="(log, index) in logs"
        :key="index"
        style="width: 1200px"
        shadow="hover"
      >
        <!-- Card header with title -->
        <div class="card-header">
          <h2>{{ log.title }}</h2>
          <!-- 显示 title -->
        </div>
        <!-- Card footer with buttons -->
        <div class="card-footer">
          <el-button type="primary" @click="openMarkdownDialog(log)">点击查看</el-button>
          <el-button type="danger" @click="deleteLog(log.log_id)">删除</el-button>
          <!-- 添加删除按钮 -->
        </div>
      </el-card>
    </div>

    <!-- 使用 ElDialog 显示 Markdown 内容 -->
    <el-dialog v-model="dialogVisible" title="日志内容" width="70%" @close="handleClose">
      <div v-html="markdownContent" class="markdown-content"></div>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="addFavorite(currentLog)">收藏</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue' // 引入生命周期钩子 onMounted
import { marked } from 'marked' // 引入marked库用于解析Markdown
import axios from 'axios' // 使用axios进行API请求
import { ElNotification } from 'element-plus'

// 定义日志类型接口
interface Log {
  log_id: string
  title: string
  content: string
}

// 存储获取的日志数据
const logs = ref<Log[]>([]) // 使用ref来存储响应式数据

// 存储弹窗显示状态和Markdown内容
const dialogVisible = ref(false)
const markdownContent = ref('')
const currentLog = ref<Log | null>(null)

// 获取日志接口数据
const getLogs = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/logs', { params: { user_id: 1 } }) // 获取用户ID为1的日志
    if (response.data && response.data.length > 0) {
      logs.value = response.data // 保存日志数据
    }
  } catch (error) {
    console.error('获取日志失败:', error)
  }
}

// 页面加载时调用获取日志函数
onMounted(() => {
  getLogs()
})

// 打开弹出框并显示解析后的 Markdown
const openMarkdownDialog = async (log: Log) => {
  markdownContent.value = await marked(log.content) // 转换Markdown为HTML
  currentLog.value = log // 保存当前日志
  dialogVisible.value = true // 确保弹窗显示
}

// 调用API添加收藏
const addFavorite = async (log: Log | null) => {
  if (!log) return
  try {
    const userId: number = 1
    await axios.post('http://127.0.0.1:8000/logs/favorites/', null, {
      params: {
        user_id: userId,
        log_id: log.log_id,
      },
    })
    successInfo('收藏成功！')
  } catch (error) {
    console.error('收藏失败:', error)
    errorInfo('收藏失败，已经收藏，或是网络原因！')
  }
}

// 删除日志
const deleteLog = async (log_id: string) => {
  try {
    const userId = 1 // 假设当前用户ID为1
    const response = await axios.delete(`http://127.0.0.1:8000/logs/${log_id}`, {
      params: {
        user_id: userId,
      },
    })

    successInfo('日志删除成功！')
    // 删除日志后重新加载日志列表
    await getLogs()
  } catch (error) {
    console.error('删除日志失败:', error)
    errorInfo('删除日志失败，请重试！')
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

// 关闭弹窗时的回调
const handleClose = () => {
  markdownContent.value = ''
}
</script>

<style scoped>
.card {
  width: 60%;
  margin: 20px auto;
}

.card-header {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.card-footer {
  text-align: right;
  /* 将所有内容右对齐 */
  position: relative;
}

.el-button {
  font-size: 1rem;
  margin-left: 10px;
  /* 给按钮添加间隔 */
}
</style>
