# -*- coding: utf - 8 - *-

import re
import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor


class Downloader():

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.95 Core/1.50.1414.400',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        # Regular match the file name
        self.r_file = re.compile(r'.*/(.*\..*)')
        # Download params
        self.download_dir = None
        self.url = None
        self.filename = None
        # Count downloaded files
        self.total = 0
        self.current = 0
        # Interrupt flag
        self.quit = False

    def start(self, url, filename=None):
        '''
        run downloader
        '''
        if not url:
            print('Doesn\'t get any download link')
            return
        self.url, self.filename, self.current = url, filename, 0
        self.__createDir()
        # start download
        st = time.clock()
        self.__downloadTask()
        ft = time.clock()
        # print result
        tt = '%.2f' % (ft - st)
        result = '|Total downloaded: %d/%d | Use time: %ss|' % (
            self.current, self.total, tt)
        n = len(result)
        print('-' * n + '\n' + result + '\n' + '-' * n)

    def __downloadTask(self):
        '''
        use threadpool to download files
        '''
        # while params are list
        if type(self.url) == list and type(self.filename) == list:
            self.total = len(self.url)
            try:
                with ThreadPoolExecutor(max_workers=8) as executor:
                    executor.submit([self.__download(e[0], e[1])
                                     for e in zip(self.url, self.filename)])
            except KeyboardInterrupt:
                print('KeyboardInterrupt ! ! !')
                self.quit = True
        # while only get url list
        elif type(self.url) == list and not self.filename:
            self.total = len(self.url)
            try:
                with ThreadPoolExecutor(max_workers=8) as executor:
                    executor.submit([self.__download(e) for e in self.url])
            except KeyboardInterrupt:
                print('KeyboardInterrupt ! ! !')
                self.quit = True
        # while params are str
        elif type(self.url) == str and type(self.filename) == str:
            self.total = 1
            self.__download(self.url, self.filename)
        # while only get url str
        elif type(self.url) == str and not self.filename:
            self.total = 1
            self.__download(self.url)
        # while params are not list or str
        else:
            print('TypeError: \'params\' object are not the same type (list or str)')

    def __download(self, url, filename=None):
        '''
        download url and save as filename
        '''
        try:
            response = requests.get(url, headers=self.headers, stream=True)
        except requests.RequestException as e:
            print(e)
            return
        if response.status_code == 404:
            print('Doesn\'t exists: ' + url)
            return
        if not filename:
            filename = self.__getFilename(url)
            filepath = self.download_dir + filename
        else:
            filepath = self.download_dir + filename
        with open(filepath, 'wb') as fp:
            print('Downloading: ' + filename)
            for block in response.iter_content(1024):
                fp.write(block)
            print('Download finished: ' + filename)
            self.current += 1
        if self.quit:
            return

    def __getFilename(self, url):
        '''
        parse filename from url
        '''
        filename = self.r_file.findall(url)[0]
        return filename

    def setDownloadDir(self, directory):
        '''
        change default download directory
        '''
        directory.replace('\\', '/')
        if directory[-1] != '/':
            directory += '/'
        self.download_dir = directory

    def __createDir(self):
        '''
        create download directory
        '''
        if not self.download_dir:
            self.download_dir = 'Download/'
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)


def main():
    img_url = 'https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/bd_logo1_31bdc765.png'
    filename = 'baidu.png'
    img_url_list = ['http://img.xiami.net/images/artistlogo/66/14585696461066.jpg',
                    'https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/bd_logo1_31bdc765.png']
    filename_list = ['music.jpg', 'baidu.jpg']
    downloader = Downloader()
	# download directory
    downloader.setDownloadDir('Test')
    # download one url
    downloader.start(img_url)
    # download a url list
    downloader.start(img_url_list, filename_list)


if __name__ == '__main__':
    main()
