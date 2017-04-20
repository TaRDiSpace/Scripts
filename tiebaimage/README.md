# tiebaimage
> 基于 Python3.5  

## 简介
为了收集壁纸贴或精美图贴中的所有图片，一次性下载下来再慢慢选，省去一页一页翻的麻烦

## 特性
- 可以解析并下载百度贴吧一个帖子中的所有图片

## 实现方法
- 原始图片url解析
``` python
img_urls = sel.xpath('//img[@class="BDE_Image"]/@src')
for img_url in img_urls:
    img_name = re.sub('.*/', '', img_url)
    download_url = 'http://imgsrc.baidu.com/forum/pic/item/' + img_name
```

## 下载安装  
- 需要安装的库
``` python
pip install lxml
pip install requests
```
- 需要导入的包  
[downloader](https://github.com/TaRDiSpace/Scripts/tree/master/downloader)

## 使用方法
> 运行输入帖子url即可

## 注意事项
暂无