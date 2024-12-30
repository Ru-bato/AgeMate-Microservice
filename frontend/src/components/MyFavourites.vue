<template>
  <div class="home-page">
    <div class="welcome-message">
      <!-- 循环展示所有已收藏的日志 -->
      <el-card class="card" v-for="(log, index) in favoriteLogs" :key="index" style="width: 1200px" shadow="hover">
        <div class="card-header">
          <h2>{{ log.title }}</h2> <!-- 显示 title -->
        </div>
        <div class="card-footer">
          <!-- 点击查看按钮打开弹窗 -->
          <el-button type="primary" @click="openMarkdownDialog(log)">点击查看</el-button>
        </div>
      </el-card>
    </div>

    <!-- 使用 ElDialog 显示 Markdown 内容 -->
    <el-dialog v-model="dialogVisible" title="日志内容" width="70%" @close="handleClose">
      <div v-html="markdownContent" class="markdown-content"></div>
      <template #footer>
        <div class="dialog-footer">
          <!-- 如果日志已经收藏，显示“取消收藏”按钮 -->
          <el-button type="danger" @click="removeFavorite(currentLog)">取消收藏</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { marked } from 'marked';
import axios from 'axios';
import { ElNotification } from 'element-plus';

// 存储已收藏的日志数据
const favoriteLogs = ref<Array<{ log_id: string, title: string, content: string }>>([]);

// 存储弹窗显示状态和Markdown内容
const dialogVisible = ref(false);
const markdownContent = ref('');
const currentLog = ref<{ log_id: string, title: string, content: string } | null>(null);

// 获取已收藏的日志数据
const getFavorites = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/logs/favorites/", {
      params: { user_id: 1 }
    });
    if (response.data && response.data.length > 0) {
      favoriteLogs.value = response.data; // 更新已收藏的日志
    }
  } catch (error) {
    console.error('获取已收藏日志失败:', error);
  }
};

// 页面加载时调用获取已收藏日志
onMounted(() => {
  getFavorites();
});

// 打开弹出框并显示解析后的 Markdown
const openMarkdownDialog = (log: { log_id: string, content: string }) => {
  markdownContent.value = marked(log.content); // 将Markdown内容转换为HTML
  currentLog.value = log; // 保存当前日志
  dialogVisible.value = true; // 打开弹窗
};

// 取消收藏操作
const removeFavorite = async (log: { log_id: string }) => {
  try {
    const userId = 1; // 假设当前用户ID为1
    const response = await axios.delete("http://127.0.0.1:8000/logs/favorites/", {
      params: {
        user_id: userId,
        log_id: log.log_id
      }
    });
    console.log(response.data);
    successInfo("取消收藏成功！");
    // 取消收藏后重新加载已收藏数据
    await getFavorites();
  } catch (error) {
    console.error('取消收藏失败:', error);
    errorInfo("取消收藏失败，请重试！");
  }
};

// 成功通知函数
const successInfo = (message: string) => {
  ElNotification({
    title: 'Success',
    message: message,
    type: 'success',
  });
}

// 错误通知函数
const errorInfo = (message: string) => {
  ElNotification({
    title: 'Error',
    message: message,
    type: 'error',
  });
}

// 关闭弹窗时的回调
const handleClose = () => {
  markdownContent.value = '';
};
</script>

<style scoped>
.card {
  width: 60%;
  margin: 20px auto;
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
</style>
