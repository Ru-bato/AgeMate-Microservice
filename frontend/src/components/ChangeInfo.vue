<template>
    <div class="edit-info-page">
        <div class="clock">
            <span>{{ currentDate }}</span>
        </div>
        <div class="background">
            <img src="@/assets/background.jpg" alt="background" />
        </div>
        <div class="edit-info-container">
            <div class="logo-container">
                <img src="@/assets/defaultavatar.jpg" alt="Logo" class="logo-image" />
            </div>
            <h2>修改个人信息</h2>
            <form @submit.prevent="handleEditInfo">
                <!-- 如果是管理员，显示目标用户名输入框 -->
                <div v-if="isAdmin" class="form-group">
                    <input type="text" id="target-username" v-model="targetUsername" placeholder="请输入要修改的用户名"
                        required />
                </div>
                <div class="form-group">
                    <input type="text" id="username" v-model="username" placeholder="请输入新用户名" required />
                </div>
                <div class="form-group">
                    <input type="password" id="password" v-model="password" placeholder="请输入新密码" required />
                </div>
                <div class="form-group">
                    <input type="password" id="checkPassword" v-model="checkPassword" placeholder="请确认新密码" required />
                </div>
                <div class="form-group">
                    <input type="text" id="phone_number" v-model="phone_number" placeholder="请输入新手机号" required />
                </div>
                <button type="submit" class="edit-info-button">提交修改</button>
            </form>
            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
            <div class="button-container">
                <button @click="goBack" class="back-button">返回</button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, defineProps } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// 接收父组件传递的 props
const props = defineProps({
    authority: {
        type: Number,
        required: true
    },
    access_token: {
        type: String,
        required: true
    },
    username: {
        type: String,
        required: true
    }
});

// 定义状态
const username = ref('');
const password = ref('');
const checkPassword = ref('');
const phone_number = ref('');
const targetUsername = ref(''); // 目标用户名（仅管理员使用）
const errorMessage = ref<string>(''); // 错误信息
const currentDate = ref<string>(getCurrentFormattedTime());
const router = useRouter();

// 判断是否为管理员
const isAdmin = Number(props.authority) === 0;

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

// 修改信息处理函数
const handleEditInfo = async () => {
    if (password.value !== checkPassword.value) {
        errorMessage.value = '密码和确认密码不一致！';
        return;
    }

    try {
        const targetUser = isAdmin ? targetUsername.value : username.value; // 管理员修改指定用户名
        // 获取用户信息
        const accountResponse = await axios.post(`http://localhost:8005/api/user/account`,
            {
                username: targetUser
            },
            {
                headers: {
                    Authorization: `Bearer ${props.access_token}`,
                }
            }
        );

        // 发送修改请求
        const response = await axios.post('http://localhost:8005/api/user/changeAccount', {
            userID: accountResponse.data.userID,
            username: username.value,
            password: password.value,
            phone_number: phone_number.value,
            authority: accountResponse.data.authority
        }, {
            headers: {
                Authorization: `Bearer ${props.access_token}`,
            }
        });

        if (response.data.status === 'success') {
            errorMessage.value = '信息修改成功！';
        } else {
            errorMessage.value = response.data.message || '修改失败，请重试！';
        }
    } catch (error) {
        console.error('修改信息失败:', error);
        errorMessage.value = '服务器错误，请尝试重新登陆后再试';
    }
};

// 返回主页
const goBack = () => {
    router.push({
        name: 'Home',
        params: { username: props.username, authority: props.authority }
    });
};

// 更新时间
setInterval(() => {
    currentDate.value = getCurrentFormattedTime();
}, 1000);
</script>

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

.edit-info-page {
    display: flex;
    height: 99vh;
    width: 100vw;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
}

.background {
    position: fixed;
    top: 0;
    left: -20%;
    right: 0;
    bottom: 0;
    z-index: -1;
}

.background img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}

.edit-info-container {
    width: auto;
    max-width: 400px;
    padding: 40px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0);
}

h2 {
    text-align: center;
    font-size: 24px;
    margin-bottom: 20px;
    color: #ddd;
    text-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
}

.logo-container {
    display: flex;
    justify-content: center;
    margin-bottom: 30px;
}

.logo-image {
    width: 95px;
    height: 95px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}

.form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
}

input::placeholder {
    color: #444;
    font: normal 14px/1.5 "MiSans", sans-serif;
}

input {
    width: 100%;
    padding: 10px;
    font-size: 14px;
    border: 1px solid #666;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    border-radius: 5px;
    background-color: rgba(255, 255, 255, 0.3);
    color: #444;
}

.edit-info-button {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    background-image: linear-gradient(45deg, #0256ed, #b20242);
    color: #ddd;
    border: 1px solid #666;
    border-radius: 5px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    cursor: pointer;
    background-size: 200% 200%;
    transition: background-position 0.4s ease;
}

.edit-info-button:hover {
    background-position: 100% 100%;
}

.back-button {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    background-color: #555;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    color: #ddd;
    border: 1px solid #666;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.4s ease;
}

.back-button:hover {
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