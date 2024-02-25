import logging
import time
from .utils import logger, request_drcom, ping


class Bocchi:
    def __init__(self,
                 username: str,
                 password: str,
                 trying_times: int,
                 drcom_url: str = 'https://drcom.szu.edu.cn/',
                 ping_url: str = 'www.baidu.com',
                 log_path: str = 'bocchi_link.log',
                 log_terminal: bool = True):
        self.username = username
        self.password = password
        self.logger = logger(log_path, log_terminal=log_terminal)
        self.drcom_url = drcom_url
        self.ping_url = ping_url
        self.trying_times = trying_times
        self.loop_time = 60
        self.logger.info('BocchiLink initialized')
        self.logger.info(self.__dict__)

    def trying(self):
        for t in range(self.trying_times):
            self.logger.info(f'{t}th checking connection...')
            if not ping(self.ping_url):
                self.logger.warning('Connection lost')
                self.logger.setLevel(logging.INFO)
                self.log_in()
            else:
                self.logger.info('Already connected. Shut down')
                break

    def loop(self):
        while True:
            self.logger.info('Checking connection...')
            if not ping(self.ping_url):
                self.logger.warning('Connection lost')
                self.logger.setLevel(logging.INFO)
                self.log_in()
            else:
                self.logger.info('Connection is good')
                self.logger.setLevel(logging.WARNING)
            self.logger.info(f'Sleeping for {self.loop_time} seconds...')
            time.sleep(self.loop_time)

    def log_in(self) -> bool:
        self.logger.info('Trying to log in...')

        data = {
            'DDDDD': self.username,
            'upass': self.password,
            '0MKKey': '123456',
            'R1': '0',
            'R2': '',
            'R6': '0',
            'para': '00',
        }

        header = {
            'Host': self.drcom_url,
            'Origin': self.drcom_url,
            'Referer': self.drcom_url + '/a70.htm',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/63.0.3239.132 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response_text, response_page_title = request_drcom(self.drcom_url, data, header)

        self.logger.info(f'Response Page Title: {response_page_title}')
        if '成功' in response_page_title:
            self.logger.info('Log in successfully')
            self.logger.setLevel(logging.WARNING)
            return True
        else:
            self.logger.warning('Log in failed')
            return False

    def log_out(self):
        self.logger.info('Trying to log out...')
        url = self.drcom_url + 'F.htm'
        response_text, response_page_title = request_drcom(url)
        self.logger.info(f'Response Page Title: {response_page_title}')
        if '失败' in response_page_title:
            self.logger.info('Log out successfully')
            return True
        else:
            self.logger.warning('Log out failed')
            return False
