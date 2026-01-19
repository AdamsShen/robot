import threading
import requests


class Download:
    def download(self, url, callback_world_count):
        print(f'线程:{threading.get_ident()} 开始下载:{url}')
        response = requests.get(url)
        response.encoding = "utf-8"
        callback_world_count(url, response.text)   # 调用回调函数
        # pass
    def start_download(self, url, callback_world_count):
        # pass
        # self.download(url, callback_world_count)
        thread = threading.Thread(target=self.download, args=(url, callback_world_count))
        thread.start()


def world_count(url, result):
    """
    world_count 的 Docstring,普通函数， 用于回调
    
    :param url: 说明
    :param result: 说明
    """
    print(f'{url}:{len(result)}->{result[:5]}')

def main():
    download = Download()
    download.start_download('http://baidu.com', world_count)
    download.start_download('http://baidu.com', world_count)
    download.start_download('http://baidu.com', world_count)