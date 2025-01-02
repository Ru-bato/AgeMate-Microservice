<template>
  <div class="home-view">
    <el-container>
      <el-header>
        <TopBar :username="username" :authority="authority" />
      </el-header>
      <el-container>
        <el-aside v-if="!route.meta.fullWidth">
          <NavBar :username="username" :authority="authority" />
        </el-aside>
        <el-main style="width: 100vw">
          <router-view @search="handleSearch"></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/NavBar.vue'
import TopBar from '@/components/TopBar.vue'
import { ref } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

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

const username = props.username
const authority = props.authority

const searchResults = ref<string[]>([])

const route = useRoute()

// 处理搜索请求
const handleSearch = async ({ query, url }: { query: string; url: string }) => {
  if (!query.trim() && !url.trim()) return

  try {
    // 假设有一个API端点用于搜索，支持query和url参数
    const response = await axios.get(`/api/search`, {
      params: {
        q: encodeURIComponent(query),
        url: encodeURIComponent(url),
      },
    })
    searchResults.value = response.data.results
  } catch (error) {
    console.error('搜索请求失败:', error)
    searchResults.value = ['未找到相关结果']
  }
}
</script>

<style scoped>
.home-view {
  display: flex;
  height: 100vh; /* 确保高度填满视口 */
  overflow: hidden; /* 防止内容溢出 */
}

.el-header {
  height: 60px; /* 上边栏高度 */
}

.el-aside {
  width: 250px; /* 侧边栏宽度 */
}

.el-main.full-width {
  flex: 1 1 100%;
}

.el-main {
  padding: 20px;
  overflow-y: auto;
  background-color: #ecf0f1;
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
