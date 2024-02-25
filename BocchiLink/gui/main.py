import PySimpleGUI as sg
from BocchiLink import Bocchi
from BocchiLink.utils import logger
import logging
import asyncio


class GUIStatusStream:
    def __init__(self, status_window):
        self.window = status_window

    def write(self, text):
        self.window.write(text)

    def flush(self):
        pass


class BocchiGUI:
    def __init__(self, link_instance: Bocchi = None):
        self.layout = [
            [sg.Text("BocchiLink", font=("Arial", 20))],
            [sg.Text("用户名: "), sg.Input(key="username")],
            [sg.Text("密码: "), sg.Input(key="password")],
            [sg.Button("登录", key="login"), sg.Button("Exit")],
            [sg.Text("状态:")],
            # 多行文本框
            [sg.Multiline(key="status", size=(50, 10))],
        ]
        self.window = sg.Window("BocchiLink", self.layout)
        self.link_instance = link_instance


    def start(self):
        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "login":
                if self.link_instance is not None:
                    del self.link_instance.logger.handlers[:]
                _usr = values["username"]
                _pwd = values["password"]
                self.window["status"].write("正在登录...")
                _status_stream = GUIStatusStream(self.window["status"])
                # _status_stream.write("111")
                _logger = logger("bocchi_link.log", log_stream=_status_stream)
                self.link_instance = Bocchi(_usr, _pwd, _logger=_logger)
                # run in a new thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.link_instance.loop_item())
            # self.window["status"].update(link_logger.)
            # print(link_logger.info)

        self.window.close()


if __name__ == "__main__":
    gui = BocchiGUI()
    gui.start()
