<<<<<<< HEAD
<template>
  <div class="login-register-view">
    <!-- 根据状态切换显示 Login 或 Register 组件 -->
    <Login v-if="isLoginView" @switchToRegister="toggleView" />
    <Register v-else @switchToLogin="toggleView" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';

// 切换状态：控制当前显示登录还是注册
const isLoginView = ref(true);

// 切换视图函数
const toggleView = () => {
  isLoginView.value = !isLoginView.value;
};
</script>

<style scoped>

</style>
=======
<template>
  <div class="login-register-view">
    <!-- 根据状态切换显示 Login 或 Register 组件 -->
    <Login v-if="isLoginView" @switchToRegister="toggleView" />
    <Register v-else @switchToLogin="toggleView" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';

// 切换状态：控制当前显示登录还是注册
const isLoginView = ref(true);

// 切换视图函数
const toggleView = () => {
  isLoginView.value = !isLoginView.value;
};
</script>

<style scoped>

</style>
>>>>>>> origin/bsh
