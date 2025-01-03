<template>
  <div class="speech-to-text">
    <h1>帮助助手</h1>
    <button @click="startRecognition" :disabled="isListening">请说话</button>
    <button @click="stopRecognition" :disabled="!isListening">结束说话</button>
    <p v-if="recognizedText">识别结果: {{ recognizedText }}</p>
    <p v-else>请点击“开始录音”按钮并说话...</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "SpeechToText",
  setup() {
    const recognizedText = ref(""); // 存储识别的文本
    const isListening = ref(false); // 是否正在录音
    let recognition: SpeechRecognition | null = null; // 语音识别对象

    // 初始化语音识别
    const initRecognition = () => {
      if (!("webkitSpeechRecognition" in window)) {
        alert("您的浏览器不支持Web Speech API，请使用Chrome浏览器。");
        return;
      }

      recognition = new (window as any).webkitSpeechRecognition();
      recognition.lang = "zh-CN"; // 设置语言为中文
      recognition.continuous = true; // 持续识别（不限制录音时间）
      recognition.interimResults = true; // 显示临时结果

      recognition.onresult = (event: SpeechRecognitionEvent) => {
        let finalTranscript = ""; // 最终识别结果
        let interimTranscript = ""; // 临时识别结果

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        // 更新识别结果
        recognizedText.value = finalTranscript || interimTranscript;
      };

      recognition.onerror = (event: SpeechRecognitionError) => {
        console.error("语音识别错误:", event.error);
        isListening.value = false;
      };

      recognition.onend = () => {
        if (isListening.value) {
          // 如果仍在录音状态，重新开始录音
          recognition?.start();
        }
      };
    };

    // 开始录音
    const startRecognition = () => {
      if (!recognition) {
        initRecognition();
      }
      recognizedText.value = ""; // 清空之前的识别结果
      isListening.value = true;
      recognition?.start();
    };

    // 停止录音
    const stopRecognition = () => {
      if (recognition) {
        recognition.stop();
        isListening.value = false;
      }
    };

    return {
      recognizedText,//文字 之后可能需要使用它
      isListening,
      startRecognition,
      stopRecognition,
    };
  },
});
</script>

<style scoped>
.speech-to-text {
  text-align: center;
  margin-top: 50px;
}

button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 16px;
}

p {
  font-size: 18px;
  margin-top: 20px;
}
</style>