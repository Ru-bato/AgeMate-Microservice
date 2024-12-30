<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'; // 引入axios



// 定义其他状态
const username = ref('');
const password = ref('');
const errorMessage = ref<string>(''); // 错误信息
const currentDate = ref<string>(getCurrentFormattedTime());
const router = useRouter();
const accountResponse = ref();

function getCurrentFormattedTime(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const week = ['日', '一', '二', '三', '四', '五', '六'][now.getDay()];
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  return `现在是 ${year}年${month}月${day}日星期${week} ${hours}:${minutes}:${seconds}`;
}

// 登录处理函数
const handleLogin = async () => {
  console.log("here try to route to home")
  router.push({ name:'Home', params: {username:'nihao', authority:1} });
  return;
  try {
    // 发送登录请求，验证用户和密码
    const loginResponse = await axios.post('/api/user/log', {
      username: username.value,
      password: password.value,
    });

    // 检查登录状态
    if (loginResponse.data.status === 'true') {
      // 登录成功，获取用户信息
      accountResponse.value = await axios.get(`/api/user/account?username=${username.value}`);
      
      const userID = accountResponse.value.data.userID;
      const authority =accountResponse.value.data.authority;

      // 跳转到主页并携带用户信息
      router.push({ name: 'Home', params: {userID:userID , username:username.value, authority:authority } });
    } else {
      // 登录失败
      errorMessage.value = loginResponse.data.message || '登录失败，请检查用户名和密码';
    }
  } catch (error) {
    console.error('登录失败:', error);
    errorMessage.value = '服务器错误，请稍后重试';
  }
};

// 更新时间
setInterval(() => {
  currentDate.value = getCurrentFormattedTime();
}, 1000);
</script>

<template>
  <div class="login-page">
    <div class="clock">
      <span>{{ currentDate }}</span>
    </div>
    <div class="background">
      <img src="@/assets/background.jpg" alt="background" />
    </div>
    <div class="login-container">
      <div class="logo-container">
        <img src="@/assets/defaultavatar.jpg" alt="Logo" class="logo-image" />
      </div>
      <h2>登录到AgeMate平台</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <input type="text" id="username" v-model="username" placeholder="请输入账号" required />
        </div>
        <div class="form-group">
          <input type="password" id="password" v-model="password" placeholder="请输入密码" required />
        </div>
        <button type="submit" class="login-button">登录</button>
      </form>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <div class="button-container">
        <button @click="$emit('switchToRegister')" class="register-button">去注册</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.clock {
  position: absolute;
  top: 35px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 18px;
  color: white;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

.login-page {
  display: flex;
  height: 99vh;
  width: 100vw;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.background {
  position:fixed;
  /* 背景绝对定位，覆盖整个页面 */
  top: 0;
  left: -20%;
  right: 0;
  bottom: 0;
  z-index: -1;
  /* 背景位于最底层 */
}

.background img {
  width: 100%;
  /* 背景图宽度占满容器 */
  height: 100%;
  /* 背景图高度占满容器 */
  object-fit: cover;
  /* 保持比例，覆盖区域 */
  object-position: center;
  /* 背景图居中 */
}

.login-container {
  width: auto;
  /* 使用 auto 让其根据内容自适应宽度 */
  max-width: 400px;
  /* 限制最大宽度 */
  padding: 40px;
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0);
  /* 设置为完全透明 */
}

h2 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  /* 调整标题与图片的间距 */
  color: #ddd;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  /* 确保图片和表单之间有足够的间距 */
}

.logo-image {
  width: 95px;
  height: 95px;
  border-radius: 50%;
  /* 圆形 */
  object-fit: cover;
  /* 保持比例，确保图片不变形 */
  border: 0 solid #333;
  /* 圆形边框 */
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  /* 添加阴影 */
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

input::placeholder {
  color: #444;
  /* 设置为你想要的颜色，例如淡灰色 */
  font: normal 14px/1.5 "MiSans", sans-serif;
}

input {
  width: 100%;
  /* 确保宽度为100% */
  padding: 10px;
  font-size: 14px;
  border: 1px solid #666;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  border-radius: 5px;
  box-sizing: border-box;
  /* 确保包含 padding 和 border 在宽度内 */
  background-color: rgba(255, 255, 255, 0.3);
  /* 半透明背景 */
  color: #444;
  /* 输入文本颜色 */
}

.login-button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  background-image: linear-gradient(45deg, #0256ed, #b20242);
  color: #ddd;
  border: 1px solid #666;
  border-radius: 5px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  cursor: pointer;
  box-sizing: border-box;
  background-size: 200% 200%;
  /* 设置背景大小以便能有渐变的移动效果 */
  transition: background-position 0.4s ease;
  /* 只针对 background-position 设置过渡 */
}

.login-button:hover {
  background-position: 100% 100%;
  /* 悬停时改变背景位置 */
}

.register-button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  background-color: #555;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  color: #ddd;
  border: 1px solid #666;
  border-radius: 5px;
  cursor: pointer;
  box-sizing: border-box;
  transition: background-color 0.4s ease;
}

.register-button:hover {
  background-color: #666666;
}

.error-message {
  color: red;
  font-size: 14px;
  text-align: center;
}

.button-container {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
}
</style>