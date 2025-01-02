// extension/contentScript.js

chrome.runtime.onMessage.addListener((data, sender, sendResponse) => {
  if (data.type === "navigation") {
    // 已经在目标网页上了，开始监听操作指令
    console.log("Ready to execute task:", data.task);
  } else {
    const { componentId, action } = data;
    const element = document.querySelector(`[data-id="${componentId}"]`);

    if (element) {
      const rect = element.getBoundingClientRect();

      // 创建对话框元素
      const dialog = document.createElement("div");
      dialog.classList.add("seeact-operation-dialog");

      // 设置对话框样式
      dialog.style.position = "absolute";
      dialog.style.top = `${rect.top + window.scrollY}px`;
      dialog.style.left = `${rect.left + window.scrollX}px`;
      dialog.style.backgroundColor = "#fff";
      dialog.style.border = "1px solid #ccc";
      dialog.style.padding = "10px";
      dialog.style.zIndex = "10000";

      // 添加操作说明
      const message = document.createElement("p");
      message.textContent = `请执行以下操作: ${action}`;
      dialog.appendChild(message);

      // 添加“执行”按钮
      const executeButton = document.createElement("button");
      executeButton.textContent = "执行";
      executeButton.id = "execute-action";
      dialog.appendChild(executeButton);

      // 添加“跳过”按钮
      const skipButton = document.createElement("button");
      skipButton.textContent = "跳过";
      skipButton.id = "skip-action";
      dialog.appendChild(skipButton);

      // 添加“自动执行”按钮
      const autoExecuteButton = document.createElement("button");
      autoExecuteButton.textContent = "自动执行";
      autoExecuteButton.id = "auto-execute";
      dialog.appendChild(autoExecuteButton);

      document.body.appendChild(dialog);

      // 监听按钮点击事件
      dialog.querySelector("#execute-action").addEventListener("click", () => {
        chrome.runtime.sendMessage({ type: "EXECUTE_ACTION", data });
        dialog.remove();
      });

      dialog.querySelector("#skip-action").addEventListener("click", () => {
        chrome.runtime.sendMessage({ type: "SKIP_ACTION", data });
        dialog.remove();
      });

      dialog.querySelector("#auto-execute").addEventListener("click", () => {
        chrome.runtime.sendMessage({ type: "AUTO_EXECUTE", data });
        dialog.remove();
      });
    }
  }
});
