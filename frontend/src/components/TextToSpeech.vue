<template>
  <div class="speech-to-text">
    <h1>帮助助手</h1>
    <div class="chat-container">
      <div v-for="(message, index) in messages" :key="index" :class="message.type">
        <div class="bubble">{{ message.text }}</div>
      </div>
    </div>
    <div class="controls">
      <button @click="startRecognition" :disabled="isListening">请说话</button>
      <button @click="stopRecognition" :disabled="!isListening">结束说话</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

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

interface Message {
  text: string
  type: 'user' | 'assistant'
}

export default defineComponent({
  name: 'SpeechToText',
  setup() {
    const messages = ref<Message[]>([]) // 存储对话消息
    const isListening = ref(false) // 是否正在录音
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
          messages.value.push({ text: finalTranscript, type: 'user' })
        } else if (interimTranscript) {
          // 如果存在临时结果，更新最后一条消息
          if (
            messages.value.length > 0 &&
            messages.value[messages.value.length - 1].type === 'user'
          ) {
            messages.value[messages.value.length - 1].text = interimTranscript
          } else {
            messages.value.push({ text: interimTranscript, type: 'user' })
          }
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

    return {
      messages,
      isListening,
      startRecognition,
      stopRecognition,
    }
  },
})
</script>

<style scoped>
.speech-to-text {
  text-align: center;
  margin-top: 50px;
}

.chat-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
  height: 400px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.user {
  align-self: flex-end;
}

.assistant {
  align-self: flex-start;
}

.bubble {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 15px;
  background-color: #e1e1e1;
  color: #333;
}

.user .bubble {
  background-color: #007bff;
  color: white;
}

.controls {
  margin-top: 20px;
}

button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
