<template>
    <div class="home-page">
        <div class="welcome-message">
            <h1>欢迎回来！</h1>
        </div>

        <div class="home-actions">
            <button @click="logout" class="logout-button">退出登录</button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// 接收来自登录页面传递的 userID 和 username
const props = defineProps({
    username: {
        type: String,
        required: true
    },
    authority: {
        type: Number,
        required: true
    }
});

const router = useRouter();

// 退出登录，跳转回登录页面
const logout = () => {
    router.push({ name: 'Login' });
};
</script>

<style scoped>
.home-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    /* background-color: #f0f0f0; */
}

.welcome-message {
    margin-bottom: 30px;
    text-align: center;
}

h1 {
    font-size: 24px;
    color: #333;
}

p {
    font-size: 18px;
    color: #666;
}

.home-actions {
    display: flex;
    gap: 20px;
}

button {
    padding: 10px 20px;
    font-size: 16px;
    border-radius: 5px;
    cursor: pointer;
    border: none;
    background-color: #4caf50;
    color: white;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #45a049;
}

.logout-button {
    background-color: #f44336;
}

.logout-button:hover {
    background-color: #e53935;
}
</style>