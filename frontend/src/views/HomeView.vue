<template>
  <!-- <div class="home-view">
    <NavBar :username="username" :authority="authority" />
    <TopBar :username="username" :authority="authority" />
    <div class="content">
      <router-view />
    </div>
  </div> -->

  <el-container>
    <el-header>
      <NavBar :username="username" :authority="authority" />
    </el-header>
    <el-container>
      <el-aside>
        <TopBar :username="username" :authority="authority" />
      </el-aside>
      <el-main><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import TopBar from '@/components/TopBar.vue'
import NavBar from '@/components/NavBar.vue'
import { defineProps } from 'vue'

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
</script>

<style scoped>
.home-view {
  display: flex;
}

.content {

  min-height: 100vh;
}
</style>
