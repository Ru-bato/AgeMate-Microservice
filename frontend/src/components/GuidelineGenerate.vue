<template>
  <div class="home-page">
    <div class="welcome-message">
      <!-- Card component 1: 基本操作 -->
      <el-card class="card" style="width: 1200px" shadow="hover">
        <!-- Card header with title -->
        <div class="card-header">
          <h2>小红书锅包肉教程指导书</h2>
        </div>

        <!-- Card body with content -->
        <div class="card-body">
          <p>如何在制作锅包肉？</p>
        </div>

        <!-- Card footer with button -->
        <div class="card-footer">
          <el-button type="primary" @click="openMarkdownDialog">点击查看</el-button>
        </div>
      </el-card>

      <el-card class="card" style="width: 1200px" shadow="hover">
        <!-- Card header with title -->
        <div class="card-header">
          <h2>淘宝购物指导书</h2>
        </div>

        <!-- Card body with content -->
        <div class="card-body">
          <p>如何在淘宝上购物？</p>
        </div>

        <!-- Card footer with button -->
        <div class="card-footer">
          <el-button type="primary" @click="openMarkdownDialog">点击查看</el-button>
        </div>
      </el-card>

      <!-- Card component 2: 文件管理 -->
      <el-card class="card" style="width: 1200px" shadow="hover">
        <!-- Card header with title -->
        <div class="card-header">
          <h2>打开b站指导书</h2>
        </div>

        <!-- Card body with content -->
        <div class="card-body">
          <p>如何打开b站？</p>
        </div>

        <!-- Card footer with button -->
        <div class="card-footer">
          <el-button type="primary" @click="openMarkdownDialog">点击查看</el-button>
        </div>
      </el-card>

      <!-- Card component 3: 浏览器使用 -->
      <el-card class="card" style="width: 1200px" shadow="hover">
        <!-- Card header with title -->
        <div class="card-header">
          <h2>查看新闻指导书</h2>
        </div>

        <!-- Card body with content -->
        <div class="card-body">
          <p>如何在在微博中查看新闻？</p>
        </div>

        <!-- Card footer with button -->
        <div class="card-footer">
          <el-button type="primary" @click="openMarkdownDialog">点击查看</el-button>
        </div>
      </el-card>

      <!-- Card component 4: 邮件操作 -->
      <el-card class="card" style="width: 1200px" shadow="hover">
        <!-- Card header with title -->
        <div class="card-header">
          <h2>发送邮件指导书</h2>
        </div>

        <!-- Card body with content -->
        <div class="card-body">
          <p>如何发送邮件？</p>
        </div>

        <!-- Card footer with button -->
        <div class="card-footer">
          <el-button type="primary" @click="openMarkdownDialog">点击查看</el-button>
        </div>
      </el-card>

      <!-- Card component 5: 安全防护 -->
      <el-card class="card" style="width: 1200px" shadow="hover">
        <!-- Card header with title -->
        <div class="card-header">
          <h2>查看天气指导书</h2>
        </div>

        <!-- Card body with content -->
        <div class="card-body">
          <p>如何查看今日天气？</p>
        </div>

        <!-- Card footer with button -->
        <div class="card-footer">
          <el-button type="primary" @click="openMarkdownDialog">点击查看</el-button>
        </div>
      </el-card>



    </div>
  </div>
</template>

<script setup lang="ts">
import { ElMessageBox, ElLoading } from 'element-plus'; // 引入Element Plus的MessageBox
import { marked } from 'marked'; // 引入marked库用于解析Markdown

// 假设你的Markdown内容
const markdownContent = `
# 小红书锅包肉教程指导书

## 第一步：打开小红书网站或应用

1. 如果你使用电脑，可以直接访问 [小红书官网](https://www.xiaohongshu.com)。
2. 如果你使用手机，可以下载并打开 **小红书** 应用。

---

## 第二步：注册/登录账户

1. 在小红书网站或应用的右上角，点击 **登录** 按钮。
2. 输入你的手机号码或邮箱，按照提示完成登录。
3. 如果没有账号，可以选择 **注册**，填写必要的信息后完成注册。

---

## 第三步：搜索锅包肉教程

1. 在小红书首页顶部的搜索框中，输入关键词“锅包肉教程”。
2. 按下 **搜索** 或点击放大镜图标，小红书会展示与关键词相关的内容。

---

## 第四步：筛选和浏览内容

1. 搜索结果页面会显示多个锅包肉相关的帖子或视频，你可以通过**热度排序**或**时间排序**找到最适合的内容。
2. 点击感兴趣的帖子，进入详细内容页面查看锅包肉的做法。

---

## 第五步：查看锅包肉教程详情

1. 在内容详情页，你可以查看博主分享的锅包肉做法，包括食材清单、步骤图解、烹饪技巧等。
2. 有些帖子还会附上教学视频，你可以直接观看并学习。

---

## 第六步：收藏或保存教程

1. 如果你觉得这个教程不错，可以点击 **收藏** 按钮，将其保存到你的收藏夹。
2. 也可以点击 **分享** 按钮，将教程发送给朋友或分享到其他平台。

---

## 第七步：互动与评论

1. 对锅包肉教程有疑问或建议时，可以在帖子下方的 **评论区** 提问或与博主互动。
2. 你还可以点赞或关注发布者，获取更多类似内容。

---

## 第八步：实践锅包肉制作

1. 根据教程准备好食材，如猪肉、糖、醋、淀粉等。
2. 按照教程步骤进行操作，从腌制肉片到调制糖醋汁，再到炸制完成。
3. 试着拍照记录你的成果，并对比博主的成品。

---

## 第九步：发布自己的锅包肉成果

1. 成功制作锅包肉后，可以在小红书发布自己的经验分享。
2. 点击 **发布** 按钮，上传你的锅包肉照片，并撰写制作心得。
3. 添加“锅包肉”相关标签，让更多用户看到你的成果。

---

## 小贴士

- 小红书有许多锅包肉教程，选择高赞或视频详细的内容，更容易上手。
- 如果是第一次尝试，建议选择简单的食材和步骤，熟悉后再优化口味。
- 不要忘记和博主互动，可能会获得更多制作技巧！
`;

// 模拟 sleep 函数
const sleep = (ms: number | undefined) => new Promise(resolve => setTimeout(resolve, ms));

// 打开弹出框并显示解析后的 Markdown
const openMarkdownDialog = async () => {
  // 开启loading动画
  const loading = ElLoading.service({
    text: '正在加载...',
    spinner: 'el-icon-loading',
    background: 'rgba(0, 0, 0, 0.1)', // 可以自定义背景色
  });

  try {
    // 模拟延迟加载1秒
    await sleep(700);

    // 关闭loading动画
    loading.close();

    // 将Markdown转换为HTML
    const htmlContent: string = await marked(markdownContent);

    // 打开弹出框并显示解析后的Markdown
    ElMessageBox({
      message: htmlContent, // 使用解析后的HTML内容
      dangerouslyUseHTMLString: true, // 允许使用HTML字符串
      confirmButtonText: '确定',
      customClass: 'markdown-dialog', // 自定义类名
    });
  } catch (error) {
    // 异常处理
    loading.close();
    console.error('加载失败:', error);
  }
};
</script>

<style scoped>
.card {
  width: 60%;
  /* Adjust the card width as per your needs */
}

.card-header {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.card-body {
  margin: 20px 0;
  font-size: 1rem;
  color: #555;
}

.card-footer {
  text-align: center;
  position: relative;
}

.el-button {
  position: absolute;
  right: 10px;
  bottom: 10px;
  font-size: 1rem;
}

/* 自定义弹框样式 */
.markdown-dialog .el-message-box__wrapper .el-message-box__content {
  width: 80%; /* 设置宽度为80%，根据需要调整 */
  max-width: 900px; /* 设置最大宽度 */
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #2c3e50;
}

/* 样式化标题 */
.markdown-dialog h1,
.markdown-dialog h2 {
  font-weight: bold;
  color: #2c3e50;
  margin-top: 20px;
  line-height: 1.5;
  /* 增加行高，优化视觉效果 */
}

.markdown-dialog h1 {
  font-size: 28px;
  margin-bottom: 10px;
}

.markdown-dialog h2 {
  font-size: 22px;
  margin-bottom: 15px;
}

/* 样式化代码块 */
.markdown-dialog pre {
  background-color: #f5f5f5;
  border-radius: 6px;
  padding: 12px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: #2d3436;
  overflow-x: auto;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
  /* 内阴影 */
}

/* 样式化列表 */
.markdown-dialog ul,
.markdown-dialog ol {
  margin-left: 20px;
  line-height: 1.8;
  color: #34495e;
}

.markdown-dialog ul li,
.markdown-dialog ol li {
  font-size: 16px;
  margin-bottom: 8px;
  /* 增加间距，提升可读性 */
}

.markdown-dialog ul li {
  list-style-type: disc;
}

.markdown-dialog ol li {
  list-style-type: decimal;
}

/* 样式化引用块 */
.markdown-dialog blockquote {
  border-left: 6px solid #3498db;
  /* 更粗的蓝色左边框 */
  padding-left: 20px;
  margin-left: 0;
  font-style: italic;
  color: #7f8c8d;
  background-color: #ecf0f1;
  font-size: 16px;
  /* 调整字体大小 */
  margin-bottom: 20px;
  /* 增加底部间距 */
}

/* 调整弹框内容的按钮样式 */
.markdown-dialog .el-message-box__btns {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.markdown-dialog .el-message-box__btns .el-button {
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
}

.markdown-dialog .el-message-box__btns .el-button--primary {
  background-color: #3498db;
  border-color: #3498db;
}

.markdown-dialog .el-message-box__btns .el-button--primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

   
   /* 如有需要，增加优先级 */
   .markdown-dialog .el-message-box__wrapper .el-message-box__content {
     width: 80% !important;
     max-width: 900px !important;
   }
</style>
