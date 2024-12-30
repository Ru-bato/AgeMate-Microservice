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
    <div class="result-box">
      <p v-if="recognizedText" class="result-text">识别结果: {{ recognizedText }}</p>
      <p v-else class="placeholder-text">请点击“开始说话”按钮并说话...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount } from 'vue'

// 定义响应式变量
const recognizedText = ref<string>('') // 存储识别的文本
const isListening = ref<boolean>(false) // 是否正在录音
let recognition: SpeechRecognition | null = null // 语音识别对象

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
    recognizedText.value = finalTranscript || interimTranscript
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
  margin-top: 50px;
  font-family: 'Arial', sans-serif;
}

.title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 20px;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
}

.button {
  padding: 12px 24px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
}

.button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.start-button {
  background-color: #4caf50;
  color: white;
}

.start-button:hover:not(:disabled) {
  background-color: #45a049;
  transform: scale(1.05);
}

.stop-button {
  background-color: #f44336;
  color: white;
}

.stop-button:hover:not(:disabled) {
  background-color: #e53935;
  transform: scale(1.05);
}

.result-box {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.result-text {
  font-size: 1.2rem;
  color: #333;
  margin: 0;
}

.placeholder-text {
  font-size: 1.2rem;
  color: #888;
  margin: 0;
}
</style>
