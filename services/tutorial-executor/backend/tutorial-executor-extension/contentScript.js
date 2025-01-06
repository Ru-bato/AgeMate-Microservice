// extension/contentScript.js

chrome.runtime.onMessage.addListener((data, sender, sendResponse) => {
  if (data.type === "START_LOADING") {
    // 创建加载动画
    const loader = document.createElement("div");
    loader.classList.add("seeact-loader-container");
    
    const spinnerContainer = document.createElement("div");
    spinnerContainer.classList.add("seeact-spinner");
    loader.appendChild(spinnerContainer);
    
    const loadingText = document.createElement("div");
    loadingText.classList.add("seeact-loading-text");
    loadingText.textContent = "正在准备下一步操作...";
    loader.appendChild(loadingText);
    
    document.body.appendChild(loader);
  } else if (data.type === "navigation") {
    // 移除加载动画
    const existingLoader = document.querySelector(".seeact-loader-container");
    if (existingLoader) {
      existingLoader.remove();
    }
    console.log("Ready to execute task:", data.task);
  } else {
    // 移除加载动画
    const existingLoader = document.querySelector(".seeact-loader-container");
    if (existingLoader) {
      existingLoader.remove();
    }
    
    const { componentId, action } = data;
    const element = document.querySelector(`[data-id="${componentId}"]`);

    if (element) {
      const rect = element.getBoundingClientRect();

      // 创建对话框元素
      const dialog = document.createElement("div");
      dialog.classList.add("seeact-operation-dialog");
      // 存储期望的组件ID
      dialog.setAttribute('data-expected-id', componentId);

      // 设置对话框位置
      dialog.style.position = "absolute";
      dialog.style.top = `${rect.bottom + window.scrollY + 10}px`; // 将对话框放在元素下方
      dialog.style.left = `${rect.left + window.scrollX}px`;
      dialog.style.zIndex = "10000";

      // 添加操作说明
      const message = document.createElement("p");
      message.textContent = `请在此处${action}`;
      dialog.appendChild(message);

      // 添加三个按钮
      const exitButton = document.createElement("button");
      exitButton.textContent = "退出";
      exitButton.classList.add("btn-exit");
      dialog.appendChild(exitButton);

      const autoButton = document.createElement("button");
      autoButton.textContent = "自动执行";
      autoButton.classList.add("btn-auto");
      dialog.appendChild(autoButton);

      const continuousButton = document.createElement("button");
      continuousButton.textContent = "连续自动执行";
      continuousButton.classList.add("btn-continuous");
      dialog.appendChild(continuousButton);

      document.body.appendChild(dialog);

      // 按钮事件监听
      exitButton.addEventListener("click", () => {
        chrome.runtime.sendMessage({ type: "EXIT_ACTION", data });
        dialog.remove();
      });

      autoButton.addEventListener("click", () => {
        chrome.runtime.sendMessage({ type: "AUTO_EXECUTE", data });
        dialog.remove();
      });

      continuousButton.addEventListener("click", () => {
        chrome.runtime.sendMessage({ type: "CONTINUOUS_AUTO_EXECUTE", data });
        dialog.remove();
      });
    }
  }
});

// 添加点击事件监听
document.addEventListener('click', (e) => {
  const clickedElement = e.target.closest('[data-id]');
  const currentDialog = document.querySelector('.seeact-operation-dialog');
  
  if (clickedElement && currentDialog) {
    const expectedId = currentDialog.getAttribute('data-expected-id');
    const clickedId = clickedElement.getAttribute('data-id');
    
    if (clickedId !== expectedId) {
      // 创建提示元素
      const tooltip = document.createElement('div');
      tooltip.classList.add('seeact-tooltip');
      tooltip.textContent = '提示：您点击的位置与指示的位置不一致，请确认操作';
      
      // 设置提示框位置
      tooltip.style.position = 'absolute';
      tooltip.style.top = `${e.clientY + window.scrollY - 40}px`;
      tooltip.style.left = `${e.clientX + window.scrollX + 20}px`;
      
      document.body.appendChild(tooltip);
      
      // 3秒后自动移除提示
      setTimeout(() => {
        tooltip.remove();
      }, 3000);
    }
  }
});
