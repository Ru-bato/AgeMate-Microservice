<template>
  <div class="login-register-view">
    <!-- 根据状态切换显示 Login 或 Register 组件 -->
    <Login v-if="loginView === 0" @switchToRegister="toggleView(1)" @switchToChange="toggleView(2)" />
    <Register v-else-if="loginView === 1" @switchToLogin="toggleView(0)" />
    <ChangeInfo v-else-if="loginView === 2" @goBack="toggleView(0)"></ChangeInfo>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';
import ChangeInfo from '@/components/ChangeInfo.vue';

const props = defineProps({
  viewNum: {
    type: Number,
    required: false,
  }
})

// 在组件挂载时，检查 props.viewNum 是否存在并设置
onMounted(() => {
  if (props.viewNum !== undefined) {
    toggleView(props.viewNum)
  }
})

// loginView 使用原始类型 number
const loginView = ref<number>(0);

// 切换视图函数，接受 number 类型参数
const toggleView = (num: number) => {
  loginView.value = num;
};
</script>

<style scoped>
</style>
