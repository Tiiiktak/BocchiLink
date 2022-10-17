import logging
import urllib.request
import urllib.parse
import re


def logger(log_path, log_terminal=True) -> logging.Logger:
    _logger = logging.getLogger()
    _logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

    if log_terminal:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        _logger.addHandler(console_handler)

    if log_path:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        _logger.addHandler(file_handler)

    return _logger


def request_drcom(url, data=None, header=None) -> (str, str):
    if data:
        data = urllib.parse.urlencode(data).encode('utf-8')
    if header:
        request = urllib.request.Request(url, data=data, headers=header)
    else:
        request = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(request)
    response_text = response.read().decode('gbk')
    response_page_title = re.match(r'.*<title>(.*)</title>.*', response_text, re.S).group(1)
    return response_text, response_page_title


def ping(url: str) -> (bool, Exception):
    try:
        urllib.request.urlopen(url, timeout=2)
        return True, None
    except Exception as e:
        return False, e
