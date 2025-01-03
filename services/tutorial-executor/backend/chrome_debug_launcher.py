import os
import sys
import subprocess
import platform
import json
import threading
import time
import socket
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QLabel, QWidget, QMessageBox, QDialog, QTextEdit)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QFont, QIcon
import requests
import logging

logger = logging.getLogger(__name__)

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('帮助')
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout(self)
        help_text = QTextEdit(self)
        help_text.setText(
            "1. 点击'启动调试模式'按钮，启动 Chrome 的调试模式。\n"
            "2. 点击'停止调试模式'按钮，停止 Chrome 的调试模式。\n"
            "3. 如果 Chrome 没有安装，程序会提醒您安装。\n"
            "4. 状态标签会显示当前调试模式的状态。"
        )
        help_text.setReadOnly(True)
        layout.addWidget(help_text)

        self.setLayout(layout)

class Worker(QObject):
    # 定义信号
    status_checked = pyqtSignal(bool)
    started = pyqtSignal()
    finished = pyqtSignal()
    chrome_terminated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True
        self.chrome_process = None
        self._thread = None
        self.status_check_timer = QTimer()  # 添加定时器
        self.status_check_timer.timeout.connect(self.check_chrome_status)
        self.status_check_timer.setInterval(5000)  # 5秒检查一次

    def start_chrome(self, chrome_path, user_data_dir):
        try:
            logger.info("开始启动Chrome...")
            
            # 检查调试模式
            logger.info("检查是否已在调试模式...")
            if self.check_debug_port():
                logger.info("Chrome已在调试模式运行")
                self.started.emit()
                self.status_check_timer.start()
                return

            # 检查现有Chrome
            logger.info("检查是否有现有Chrome进程...")
            if self.check_existing_chrome():
                logger.info("发现现有Chrome进程，准备关闭...")
                self.kill_existing_chrome()
                logger.info("现有Chrome进程已关闭")

            # 启动新实例
            logger.info(f"启动新的Chrome实例，路径: {chrome_path}")
            cmd = [
                chrome_path,
                '--remote-debugging-port=9222',
                '--remote-debugging-address=0.0.0.0',
                '--remote-allow-origins=*',
                '--no-first-run',
                '--no-default-browser-check',
                f'--user-data-dir={user_data_dir}'
            ]
            logger.info(f"执行命令: {' '.join(cmd)}")
            self.chrome_process = subprocess.Popen(cmd)
            logger.info("Chrome进程已启动")
            self.started.emit()
            self.status_check_timer.start()
            
        except Exception as e:
            logger.error(f"Chrome启动错误: {str(e)}", exc_info=True)
            self.finished.emit()

    def check_chrome_status(self):
        """异步检查Chrome状态"""
        if not self.running:
            self.status_check_timer.stop()
            return

        if self.chrome_process and self.chrome_process.poll() is not None:
            self.chrome_terminated.emit()
            self.status_check_timer.stop()
            return

        QTimer.singleShot(0, self._check_debug_port)

    def _check_debug_port(self):
        """异步检查调试端口"""
        try:
            response = requests.get('http://localhost:9222/json/version', timeout=1)
            self.status_checked.emit(response.status_code == 200)
        except requests.RequestException:
            self.status_checked.emit(False)

    def stop_chrome(self):
        """停止Chrome进程"""
        self.running = False
        self.status_check_timer.stop()
        if self.chrome_process:
            try:
                self.chrome_process.terminate()
                # 给进程一些时间来正常终止
                QTimer.singleShot(2000, self._force_kill_if_needed)
            except Exception as e:
                logger.error(f"停止Chrome时出错: {str(e)}")
                self.finished.emit()

    def _force_kill_if_needed(self):
        """如果进程还在运行，强制结束它"""
        if self.chrome_process and self.chrome_process.poll() is None:
            try:
                self.chrome_process.kill()
            except Exception as e:
                logger.error(f"强制终止Chrome时出错: {str(e)}")
            finally:
                self.chrome_process = None
                self.finished.emit()

    def check_debug_port(self):
        """检查调试端口是否已经在使用"""
        try:
            response = requests.get('http://localhost:9222/json/version', timeout=1)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def check_existing_chrome(self):
        """检查现有的Chrome进程"""
        if platform.system() == 'Windows':
            try:
                output = subprocess.check_output(['tasklist', '/FI', 'IMAGENAME eq chrome.exe'], 
                                              stderr=subprocess.DEVNULL,
                                              encoding='gbk')  # 使用 GBK 编码
                return 'chrome.exe' in output
            except subprocess.CalledProcessError:
                logger.error("执行tasklist命令失败", exc_info=True)
                return False
            except Exception as e:
                logger.error(f"检查Chrome进程失败: {str(e)}", exc_info=True)
                return False
        else:
            try:
                output = subprocess.check_output(['pgrep', 'chrome']).decode()
                return bool(output.strip())
            except:
                logger.error("检查Chrome进程失败", exc_info=True)
                return False

    def kill_existing_chrome(self):
        """终止现有的Chrome进程"""
        try:
            logger.info("尝试终止现有Chrome进程...")
            if platform.system() == 'Windows':
                subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], 
                             check=True, 
                             stderr=subprocess.DEVNULL)
            else:
                subprocess.run(['pkill', 'chrome'], check=True)
            
            # 等待进程完全终止
            time.sleep(2)
            logger.info("Chrome进程已终止")
            
        except subprocess.CalledProcessError:
            logger.warning("终止Chrome进程时出现错误，进程可能已经不存在")
        except Exception as e:
            logger.error(f"终止Chrome进程时出现未知错误: {str(e)}", exc_info=True)

class ChromeDebugLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.chrome_process = None
        self.worker = Worker()
        self.worker_thread = QThread()
        self.setup_worker()
        
        # 移除原有的check_timer
        # self.check_timer = QTimer()
        # self.check_timer.timeout.connect(self.check_debug_status)
        # self.check_timer.start(5000)

    def setup_worker(self):
        """设置工作线程"""
        self.worker.moveToThread(self.worker_thread)
        self.worker.status_checked.connect(self.update_status)
        self.worker.started.connect(self.on_started)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.chrome_terminated.connect(self.on_chrome_terminated)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle('Chrome 调试模式启动器')
        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon('chrome_icon.png'))  # 窗口图标
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # 创建标题标签
        title_label = QLabel('Chrome 调试模式启动器')
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建状态标签
        self.status_label = QLabel('未启动')
        self.status_label.setFont(QFont('Arial', 12))
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 创建启动按钮
        self.start_button = QPushButton('启动调试模式')
        self.start_button.setFont(QFont('Arial', 12))
        self.start_button.setFixedSize(200, 50)
        self.start_button.clicked.connect(self.start_chrome_debug)
        layout.addWidget(self.start_button)
        
        # 创建停止按钮
        self.stop_button = QPushButton('停止调试模式')
        self.stop_button.setFont(QFont('Arial', 12))
        self.stop_button.setFixedSize(200, 50)
        self.stop_button.clicked.connect(self.stop_chrome_debug)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)
        
        # 创建帮助按钮
        self.help_button = QPushButton('帮助')
        self.help_button.setFont(QFont('Arial', 12))
        self.help_button.setFixedSize(200, 50)
        self.help_button.clicked.connect(self.show_help)
        layout.addWidget(self.help_button)

    def find_chrome_path(self):
        """查找Chrome可执行文件的路径"""
        system = platform.system()
        
        if system == 'Windows':
            paths = [
                os.path.join(os.environ.get('PROGRAMFILES', ''), 'Google/Chrome/Application/chrome.exe'),
                os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Google/Chrome/Application/chrome.exe'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google/Chrome/Application/chrome.exe')
            ]
        elif system == 'Darwin':  # macOS
            paths = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                os.path.expanduser('~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
            ]
        else:  # Linux
            paths = [
                '/usr/bin/google-chrome',
                '/usr/bin/google-chrome-stable',
                '/usr/bin/chromium-browser',
                '/usr/bin/chromium'
            ]
            
        for path in paths:
            if os.path.exists(path):
                return path
                
        return None

    def check_debug_status(self):
        """异步检查调试状态"""
        QTimer.singleShot(0, self._do_check_debug_status)
        
    def _do_check_debug_status(self):
        """实际执行调试状态检查"""
        try:
            response = requests.get('http://localhost:9222/json/version', timeout=1)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def start_chrome_debug(self):
        """启动Chrome调试模式"""
        if self.check_debug_status():
            self.status_label.setText('调试模式已经运行中')
            self.stop_button.setEnabled(True)
            self.start_button.setEnabled(False)
            return True

        chrome_path = self.find_chrome_path()
        if not chrome_path:
            QMessageBox.critical(self, '错误', '未找到Chrome浏览器，请确保已安装Chrome。')
            return False

        try:
            # 获取用户数据目录
            user_data_dir = self.get_user_data_dir()
            
            # 在新线程中启动Chrome
            self.worker.running = True
            self.worker_thread.start()
            QTimer.singleShot(0, lambda: self.worker.start_chrome(chrome_path, user_data_dir))
            
            return True
                
        except Exception as e:
            QMessageBox.critical(self, '错误', f'启动Chrome失败：{str(e)}')
            return False

    def stop_chrome_debug(self):
        """停止Chrome调试模式"""
        try:
            self.worker.running = False
            self.worker.stop_chrome()
            self.status_label.setText('已停止')
            self.stop_button.setEnabled(False)
            self.start_button.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'停止Chrome失败：{str(e)}')

    def update_status(self, is_running):
        """更新状态标签"""
        if is_running:
            self.status_label.setText('调试模式运行中')
            self.stop_button.setEnabled(True)
        else:
            self.status_label.setText('未运行')
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def on_started(self):
        """启动后状态更新"""
        self.start_button.setEnabled(False)
        self.status_label.setText('正在启动...')
    
    def on_chrome_terminated(self):
        """处理Chrome被手动关闭的情况"""
        QMessageBox.warning(self, '警告', 'Chrome 已被手动关闭。')
        self.status_label.setText('未运行')
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def show_help(self):
        """显示帮助窗口"""
        help_dialog = HelpDialog()
        help_dialog.exec_()

    def closeEvent(self, event):
        """窗口关闭时的处理"""
        # self.remove_port_forwarding()
        if self.chrome_process:
            self.stop_chrome_debug()
        event.accept()

    def get_user_data_dir(self):
        """获取Chrome用户数据目录"""
        if platform.system() == "Windows":
            return os.path.expanduser('~') + "/AppData/Local/Google/Chrome/User Data"
        elif platform.system() == "Darwin":
            return os.path.expanduser('~') + "/Library/Application Support/Google/Chrome"
        else:  # Linux
            return os.path.expanduser('~') + "/.config/google-chrome"

def main():
    app = QApplication(sys.argv)
    launcher = ChromeDebugLauncher()
    launcher.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()