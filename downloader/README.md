# downloader
> 基于 Python3.5

## 简介 
利用 python3.5 的 concurrent.futures 包进行多线程下载

## 特性
- 可以传入单个url进行下载，同时可以传入一个文件名（可选）
- 可以传入一个url列表进行下载，同时可以传入一个文件名列表（可选）
- 未传入文件名可自动根据url进行解析文件名

## 实现方法
- 多线程下载
``` python
from concurrent.futures import ThreadPoolExecutor
try:
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.submit([self.__download(e) for e in self.url])
except KeyboardInterrupt:
    print('KeyboardInterrupt ! ! !')
    self.quit = True
```

## 下载安装  
- 需要安装的库
``` python
pip install requests
```

## 使用方法
> downloader = Downloader()  
> downloader.setDownloadDir(directory) 设置下载目录  
> downloader.start(url, filename) 开始下载url

## 注意事项
1. url需要包含 xxx.扩展名, 否则无法解析文件名
2. 下载会默认在同目录自动创建一个Download文件夹