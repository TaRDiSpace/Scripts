# -*- coding: utf - 8 - *-

import re
import time
import requests
from lxml import etree
from concurrent import futures
from download import Downloader


class TiebaImage():

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.95 Core/1.50.1414.400',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        # 贴子页数
        self.page_param = '?pn=%d'
        # 所有图片url列表
        self.all_urls = []
        # 解析到的图片数量
        self.img_num = 0
        # 中断flag
        self.quit = False

    def getImgUrls(self, tie_url):
        '''
        返回包含所有图片url的列表
        '''
        page_urls = self.getPages(tie_url)
        if not page_urls:
            return
        print('正在解析图片url中。。。')
        try:
            with futures.ThreadPoolExecutor(max_workers=8) as executor:
                result = executor.map(self.parseUrls, page_urls)
        except KeyboardInterrupt:
            print('KeyboardInterrupt ! ! !')
            self.quit = True
        print('\n全部解析完成')
        return self.all_urls

    def getPages(self, tie_url):
        '''
        返回包含帖子所有页面url的列表
        '''
        page_urls = []
        try:
            response = requests.get(tie_url, headers=self.headers)
        except:
            print('无法访问网页！！！')
            return
        sel = etree.HTML(response.text)
        if sel.xpath('//body[@class="page404"]'):
            print('贴子不存在！！！')
            return
        num = int(
            sel.xpath('//ul[@class="l_posts_num"]/li[2]/span[2]/text()')[0])
        for i in range(1, num + 1):
            page_url = tie_url + self.page_param % i
            page_urls.append(page_url)
        return page_urls

    def parseUrls(self, page_url):
        '''
        解析每个页面包含的图片url
        '''
        try:
            response = requests.get(page_url, headers=self.headers)
        except requests.RequestException as e:
            print(e)
            return
        sel = etree.HTML(response.text)
        img_urls = sel.xpath('//img[@class="BDE_Image"]/@src')
        for img_url in img_urls:
            if self.quit:
                break
            img_name = re.sub('.*/', '', img_url)
            download_url = 'http://imgsrc.baidu.com/forum/pic/item/' + img_name
            self.img_num += 1
            print('\r获取到 %d 个图片链接' % self.img_num, end='')
            self.all_urls.append(download_url)


def main():
    # tie_url = 'http://tieba.baidu.com/p/4774287212'
    tie_url = input('请输入帖子url：')
    tiebaimg = TiebaImage()
    img_url_list = tiebaimg.getImgUrls(tie_url)
    if not img_url_list:
        print('未解析到图片url！！！')
        return
    downloader = Downloader()
    downloader.start(img_url_list)


if __name__ == '__main__':
    main()
    if input('按任意键继续。。。'):
        pass
