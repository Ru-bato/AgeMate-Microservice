const SOCKET_SERVER_URL = "ws://localhost/tutorial-executor/ws"; // 确保与后端 WebSocket 端口一致
let socket;
let heartbeatInterval;

// 获取公网IP
async function getPublicIP() {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        return data.ip;
    } catch (error) {
        console.error('获取公网IP失败:', error);
        return null;
    }
}

// 检查Chrome调试模式是否开启
async function checkDebuggerStatus() {
    try {
        const response = await fetch('http://localhost:9222/json/version');
        return response.ok;
    } catch (error) {
        return false;
    }
}

// 函数：初始化 WebSocket 连接
function initWebSocket() {
    socket = new WebSocket(SOCKET_SERVER_URL);

    // 监听 WebSocket 打开事件
    socket.addEventListener('open', async () => {
        console.log("[WebSocket] 已连接到 SeeAct 后端 WebSocket 服务器");
        startHeartbeat(); // 启动心跳机制
        
        // 连接成功后立即报告状态
        // const isDebuggerEnabled = await checkDebuggerStatus();
        // const publicIP = await getPublicIP();
        
        // if (isDebuggerEnabled) {
        //     socket.send(JSON.stringify({
        //         type: "register_client",
        //         // ip: publicIP,
        //         // debuggerEnabled: true
        //     }));
        // }
    });

    // 监听 WebSocket 消息
    socket.addEventListener('message', (event) => {
        console.log("[WebSocket] 收到操作指令:", event.data);
        try {
            const data = JSON.parse(event.data);
            if (!data || !data.type) {
                console.warn("[WebSocket] 消息格式无效，已忽略:", data);
                return;
            }
            // 将操作指令发送到当前活动标签页的内容脚本
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                if (tabs.length > 0) {
                    chrome.tabs.sendMessage(tabs[0].id, data);
                } else {
                    console.warn("[WebSocket] 无法获取活动标签页");
                }
            });
        } catch (error) {
            console.error("[WebSocket] 消息解析失败:", error);
        }
    });

    // 监听 WebSocket 关闭事件
    socket.addEventListener('close', () => {
        console.warn("[WebSocket] 与后端 WebSocket 服务器断开连接");
        stopHeartbeat(); // 停止心跳机制
        setTimeout(initWebSocket, 1000); // 断开后1秒重连
    });

    // 监听 WebSocket 错误事件
    socket.addEventListener('error', (error) => {
        console.error("[WebSocket] 发生错误:", error);
        socket.close();
    });
}

// 启动 WebSocket 心跳机制
function startHeartbeat() {
    heartbeatInterval = setInterval(async () => {
        if (socket.readyState === WebSocket.OPEN) {
            // const isDebuggerEnabled = await checkDebuggerStatus();
            // const publicIP = await getPublicIP();
            
            socket.send(JSON.stringify({ 
                type: "heartbeat",
                // ip: publicIP,
                // debuggerEnabled: isDebuggerEnabled
            }));
            console.log("[WebSocket] 发送心跳包");
        }
    }, 30000); // 每 30 秒发送一次心跳包
}

// 停止 WebSocket 心跳机制
function stopHeartbeat() {
    if (heartbeatInterval) {
        clearInterval(heartbeatInterval);
    }
}

// 初始化 WebSocket 连接
initWebSocket();