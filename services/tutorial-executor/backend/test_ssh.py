import paramiko
from sshtunnel import SSHTunnelForwarder
import os

def create_local_reverse_ssh_tunnel(local_bind_port, remote_bind_port):
    try:
        tunnel = SSHTunnelForwarder(
            ('localhost', 22),  # 本地 SSH 服务器地址和端口
            ssh_username='admin',  # 替换为你的本地用户名
            ssh_pkey=os.path.expanduser('~/.ssh/id_rsa'),  # 私钥路径
            remote_bind_address=('localhost', local_bind_port),  # 本地 Chrome 调试端口
            local_bind_address=('localhost', remote_bind_port)  # 映射到的本地端口
        )
        tunnel.start()
        print(f"Local reverse SSH tunnel established from {remote_bind_port} to {local_bind_port}")
        return tunnel
    except Exception as e:
        print(f"Failed to establish local reverse SSH tunnel: {e}")
        raise

if __name__ == "__main__":
    local_bind_port = 9222  # 本地 Chrome 调试端口
    remote_bind_port = 10022  # 想要映射到的本地端口

    tunnel = create_local_reverse_ssh_tunnel(local_bind_port, remote_bind_port)

    try:
        input("Press Enter to close the tunnel...\n")
    finally:
        tunnel.close()
        print("Tunnel closed.")

# import subprocess
# import time
# import sys


# def run_command(command):
#     try:
#         result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         print(result.stdout)
#     except subprocess.CalledProcessError as e:
#         print(f"命令执行失败: {e.stderr}")
#         sys.exit(1)


# def install_openssh():
#     print("正在检查并安装 OpenSSH 服务端...")
#     # 检查是否已经安装 OpenSSH 服务端
#     check_command = ['powershell', 'Get-WindowsCapability', '-Online', '|', 'Where-Object', '{ $_.Name -like "OpenSSH.Server*" }']
#     result = subprocess.run(check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     if "Installed" not in result.stdout:
#         # 未安装，进行安装
#         install_command = ['powershell', 'Add-WindowsCapability', '-Online', '-Name', 'OpenSSH.Server~~~~0.0.1.0']
#         run_command(install_command)
#     else:
#         print("OpenSSH 服务端已经安装。")


# def start_openssh():
#     print("正在启动 OpenSSH 服务端...")
#     # 启动 OpenSSH 服务端
#     start_command = ['powershell', 'Start-Service', '"OpenSSH SSH Server"']
#     run_command(start_command)


# def configure_firewall():
#     print("正在配置防火墙规则...")
#     # 创建防火墙入站规则
#     firewall_command = ['powershell', 'New-NetFirewallRule', '-Name', '"Allow SSH Inbound"', '-DisplayName', '"Allow SSH Inbound"',
#                       '-Enabled', 'True', '-Direction', 'Inbound', '-Protocol', 'TCP', '-Action', 'Allow', '-LocalPort', '22']
#     run_command(firewall_command)


# def main():
#     install_openssh()
#     start_openssh()
#     configure_firewall()
#     print("OpenSSH 服务端已安装并启动，防火墙规则已配置。")
#     # 等待一段时间，确保服务启动完成
#     time.sleep(5)


# if __name__ == "__main__":
#     main()
