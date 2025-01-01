import socket
import subprocess
import requests
import platform
import time
from urllib.parse import urlparse

def get_public_ip():
    """获取公网 IP 地址"""
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json().get('ip')
    except requests.RequestException as e:
        print(f"获取公网 IP 失败: {e}")
        return None

def get_local_ip():
    """获取本机内网 IP 地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # 连接到 Google 公共 DNS 服务器
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error as e:
        print(f"获取内网 IP 失败: {e}")
        return None

def setup_port_forwarding(local_ip, port):
    """配置端口转发"""
    try:
        if platform.system() == 'Windows':
            # 检查是否有管理员权限
            subprocess.run(['netsh', 'interface', 'show', 'interface'], check=True, capture_output=True)
            
            # 删除可能存在的旧规则
            subprocess.run([
                'netsh', 'interface', 'portproxy', 'delete', 'v4tov4',
                'listenport={}'.format(port), 'listenaddress=0.0.0.0'
            ], capture_output=True)
            
            # 设置端口转发规则
            command = [
                'netsh', 'interface', 'portproxy',
                'add', 'v4tov4',
                'listenport={}'.format(port),
                'listenaddress=0.0.0.0',
                'connectport={}'.format(port),
                'connectaddress={}'.format(local_ip)
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"设置端口转发失败: {result.stderr}")

            # 添加防火墙规则
            firewall_commands = [
                # 入站规则
                [
                    'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                    'name=ChromeDebugPort-In',
                    'dir=in',
                    'action=allow',
                    'protocol=TCP',
                    'localport={}'.format(port)
                ],
                # 出站规则
                [
                    'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                    'name=ChromeDebugPort-Out',
                    'dir=out',
                    'action=allow',
                    'protocol=TCP',
                    'localport={}'.format(port)
                ]
            ]
            
            for cmd in firewall_commands:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"设置防火墙规则失败: {result.stderr}")

            # 返回配置成功信息
            return True
        else:
            print("目前仅支持 Windows 系统")
            return False
    except Exception as e:
        print(f"设置端口转发失败: {e}")
        return False

def main():
    # 获取公网 IP 和内网 IP
    public_ip = get_public_ip()
    if public_ip:
        print(f"公网 IP 地址: {public_ip}")
    else:
        print("无法获取公网 IP，程序终止。")
        return

    local_ip = get_local_ip()
    if local_ip:
        print(f"内网 IP 地址: {local_ip}")
    else:
        print("无法获取内网 IP，程序终止。")
        return

    # 设置端口转发
    port = 9222
    if setup_port_forwarding(local_ip, port):
        print(f"成功配置端口转发：{public_ip}:{port} -> {local_ip}:{port}")
    else:
        print("端口转发设置失败。")

if __name__ == '__main__':
    main()
