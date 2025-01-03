<template>
  <div class="speech-to-text">
    <h1 class="title">帮助助手</h1>
    <div class="buttons">
      <button @click="startRecognition" :disabled="isListening" class="button start-button">
        🎤 开始说话
      </button>
      <button @click="stopRecognition" :disabled="!isListening" class="button stop-button">
        ⏹️ 结束说话
      </button>
    </div>
    <div class="input-box">
      <input
        type="text"
        v-model="urlInput"
        placeholder="请输入或粘贴URL"
        class="url-input"
      />
    </div>
    <div class="result-box">
      <textarea
        v-if="recognizedText"
        v-model="recognizedText"
        class="result-text"
        placeholder="识别结果会显示在这里，可以进行编辑..."
      ></textarea>
      <p v-else class="placeholder-text">请点击“开始说话”按钮并说话...</p>
    </div>
    <div class="search-button">
      <button @click="startSeeAct(recognizedText, urlInput)" class="button search-button">
        🔍 搜索
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount, defineEmits } from 'vue'
import axios from 'axios'

// 添加 Web Speech API 类型声明
declare global {
  interface Window {
    webkitSpeechRecognition: any;
    SpeechRecognition: any;
  }
  
  interface SpeechRecognitionEvent extends Event {
    results: SpeechRecognitionResultList;
    resultIndex: number;
  }

  interface SpeechRecognitionError extends Event {
    error: string;
  }
}

// 添加 Chrome API 类型声明
declare const chrome: {
  runtime: {
    sendMessage: (message: any) => Promise<any>;
  };
};

const emit = defineEmits(['search'])

// 定义响应式变量
const recognizedText = ref<string>('') // 存储识别的文本
const isListening = ref<boolean>(false) // 是否正在录音
const urlInput = ref<string>('') // 存储用户输入的URL
let recognition: Window['SpeechRecognition'] | null = null // 语音识别对象

// 初始化语音识别
const initRecognition = () => {
  if (!('webkitSpeechRecognition' in window)) {
    alert('您的浏览器不支持Web Speech API，请使用Chrome浏览器。')
    return
  }

  recognition = new (window as any).webkitSpeechRecognition()
  recognition.lang = 'zh-CN' // 设置语言为中文
  recognition.continuous = true // 持续识别（不限制录音时间）
  recognition.interimResults = true // 显示临时结果

  recognition.onresult = (event: SpeechRecognitionEvent) => {
    let finalTranscript = '' // 最终识别结果
    let interimTranscript = '' // 临时识别结果

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript
      if (event.results[i].isFinal) {
        finalTranscript += transcript
      } else {
        interimTranscript += transcript
      }
    }

    // 更新识别结果
    if (finalTranscript) {
      recognizedText.value = finalTranscript
    } else {
      recognizedText.value = interimTranscript
    }
  }

  recognition.onerror = (event: SpeechRecognitionError) => {
    console.error('语音识别错误:', event.error)
    isListening.value = false
  }

  recognition.onend = () => {
    if (isListening.value) {
      // 如果仍在录音状态，重新开始录音
      recognition?.start()
    }
  }
}

// 开始录音
const startRecognition = () => {
  if (!recognition) {
    initRecognition()
  }
  recognizedText.value = '' // 清空之前的识别结果
  isListening.value = true
  recognition?.start()
}

// 停止录音
const stopRecognition = () => {
  if (recognition) {
    recognition.stop()
    isListening.value = false
  }
}

// 触发搜索事件
const emitSearch = async () => {
  emit('search', { query: recognizedText.value, url: urlInput.value })

  // 调用后端接口，触发SeeAct操作
  try {
    const response = await axios.post('localhost/tutorial-executor/execute', {
      query: recognizedText.value,
      url: urlInput.value
    })
    console.log('SeeAct执行结果:', response.data)
  } catch (error) {
    console.error('触发SeeAct执行失败:', error)
  }
}

async function startSeeAct(query: string, url: string) {
    try {
        // 首先获取用户IP
        const ipResponse = await fetch('https://api.ipify.org?format=json');
        const ipData = await ipResponse.json();
        const userIP = ipData.ip;

        // 发送请求到后端，包含用户IP
        const response = await fetch('http://localhost/tutorial-executor/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                url: url,
                clientIP: userIP  // 添加用户IP
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '启动 SeeAct 失败');
        }

        const data = await response.json();
        console.log('SeeAct 启动状态:', data.status);
        
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    } catch (error) {
        console.error('启动 SeeAct 时出错:', error);
        throw error;
    }
}

// 在组件卸载前停止识别
onBeforeUnmount(() => {
  if (recognition) {
    recognition.stop()
  }
})
</script>

<style scoped>
.speech-to-text {
  text-align: center;
  margin-top: 5vh;
  font-family: 'Arial', sans-serif;
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  font-size: 3rem;
  color: #000;
  margin-bottom: 30px;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.button {
  padding: 20px 40px;
  font-size: 1.5rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

.button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

.start-button {
  background-color: #28a745;
  color: white;
}

.start-button:hover:not(:disabled) {
  background-color: #218838;
  transform: scale(1.05);
}

.stop-button {
  background-color: #dc3545;
  color: white;
}

.stop-button:hover:not(:disabled) {
  background-color: #c82333;
  transform: scale(1.05);
}

.search-button {
  background-color: #2980b9;
  color: white;
}

.search-button:hover {
  background-color: #2980b9;
  transform: scale(1.05);
}

.input-box {
  margin-bottom: 20px;
}

.url-input {
  width: 80%;
  max-width: 600px;
  padding: 10px 15px;
  font-size: 1.2rem;
  border: 2px solid #ccc;
  border-radius: 8px;
  outline: none;
}

.url-input:focus {
  border-color: #66afe9;
}

.result-box {
  background-color: #ffffff;
  border: 2px solid #000;
  border-radius: 15px;
  padding: 20px;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  min-height: 200px;
}

.result-text {
  width: 100%;
  height: 100px;
  font-size: 1.8rem;
  color: #000;
  border: none;
  outline: none;
  resize: vertical;
}

.placeholder-text {
  font-size: 1.8rem;
  color: #555;
  margin: 0;
}

.search-button {
  margin-top: 20px;
}
</style>
