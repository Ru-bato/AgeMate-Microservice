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

        <!-- Card footer with button -->
        <div class="card-footer">
          <el-button type="primary" @click="openMarkdownDialog(log)">点击查看</el-button>
          <el-button type="danger" @click="deleteLog(log.log_id)">删除</el-button>
          <!-- 添加删除按钮 -->
        </div>
      </el-card>

      <!-- Card component 5: 安全防护 -->
      <el-card class="card" style="width: 1200px" shadow="hover">
        <!-- Card header with title -->
        <div class="card-header">
          <h2>查看天气指导书</h2>
        </div>

        <!-- Card body with content -->
        <div class="card-body">
          <p>如何查看今日天气？</p>
        </div>

        <!-- Card footer with button -->
        <div class="card-footer">
          <el-button type="primary" @click="openMarkdownDialog">点击查看</el-button>
        </div>
      </el-card>



    </div>
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
  /* Adjust the card width as per your needs */
}

.card-header {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.card-body {
  margin: 20px 0;
  font-size: 1rem;
  color: #555;
}

.card-footer {
  text-align: center;
  position: relative;
}

.el-button {
  position: absolute;
  right: 10px;
  bottom: 10px;
  font-size: 1rem;
}

/* 自定义弹框样式 */
.markdown-dialog .el-message-box__wrapper .el-message-box__content {
  width: 80%; /* 设置宽度为80%，根据需要调整 */
  max-width: 900px; /* 设置最大宽度 */
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #2c3e50;
}

/* 样式化标题 */
.markdown-dialog h1,
.markdown-dialog h2 {
  font-weight: bold;
  color: #2c3e50;
  margin-top: 20px;
  line-height: 1.5;
  /* 增加行高，优化视觉效果 */
}

.markdown-dialog h1 {
  font-size: 28px;
  margin-bottom: 10px;
}

.markdown-dialog h2 {
  font-size: 22px;
  margin-bottom: 15px;
}

/* 样式化代码块 */
.markdown-dialog pre {
  background-color: #f5f5f5;
  border-radius: 6px;
  padding: 12px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: #2d3436;
  overflow-x: auto;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
  /* 内阴影 */
}

/* 样式化列表 */
.markdown-dialog ul,
.markdown-dialog ol {
  margin-left: 20px;
  line-height: 1.8;
  color: #34495e;
}

.markdown-dialog ul li,
.markdown-dialog ol li {
  font-size: 16px;
  margin-bottom: 8px;
  /* 增加间距，提升可读性 */
}

.markdown-dialog ul li {
  list-style-type: disc;
}

.markdown-dialog ol li {
  list-style-type: decimal;
}

/* 样式化引用块 */
.markdown-dialog blockquote {
  border-left: 6px solid #3498db;
  /* 更粗的蓝色左边框 */
  padding-left: 20px;
  margin-left: 0;
  font-style: italic;
  color: #7f8c8d;
  background-color: #ecf0f1;
  font-size: 16px;
  /* 调整字体大小 */
  margin-bottom: 20px;
  /* 增加底部间距 */
}

/* 调整弹框内容的按钮样式 */
.markdown-dialog .el-message-box__btns {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.markdown-dialog .el-message-box__btns .el-button {
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
}

.markdown-dialog .el-message-box__btns .el-button--primary {
  background-color: #3498db;
  border-color: #3498db;
}

.markdown-dialog .el-message-box__btns .el-button--primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

   
   /* 如有需要，增加优先级 */
   .markdown-dialog .el-message-box__wrapper .el-message-box__content {
     width: 80% !important;
     max-width: 900px !important;
   }
</style>
