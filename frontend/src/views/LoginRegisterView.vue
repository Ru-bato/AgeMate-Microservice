<template>
  <div class="login-register-view">
    <!-- 根据状态切换显示 Login 或 Register 组件 -->
    <Login v-if="loginView === 0" @switchToRegister="toggleView(1)"/>
    <Register v-else-if="loginView === 1" @switchToLogin="toggleView(0)" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';

const props = defineProps({
  authority: {
    type: Number,
    require: false,
  },
  username: {
    type: String,
    required: true
  }
})



// loginView 使用原始类型 number
const loginView = ref<number>(0);

// 切换视图函数，接受 number 类型参数
const toggleView = (num: number) => {
  loginView.value = num;
};
</script>

<style scoped></style>
