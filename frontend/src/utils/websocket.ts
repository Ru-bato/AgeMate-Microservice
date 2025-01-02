// frontend/src/utils/websocket.ts

import { io } from "socket.io-client";

const socket = io("http://localhost:tutorial-executor"); // 调整为您的后端地址

export default socket;