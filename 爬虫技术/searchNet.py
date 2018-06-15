#coding=utf-8
import requests #爬虫工具
from bs4 import BeautifulSoup #爬虫工具，主要是从网页上抓取数据，提取xml、html标签的内容； Soup=汤，或者软件更新程序包
import os
import traceback

def download(url, filename):
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        r = requests.get(url, stream=True, timeout=60)# 用timeout变量来配置最大请求时间，
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return filename
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()
        if os.path.exists(filename):
            os.remove(filename)


if os.path.exists('imgs') is False:
    os.makedirs('imgs')

start = 1
end = 8000
for i in range(start, end + 1):
    #url = 'http://konachan.net/post?page=%d&tags=' % i
    url = 'http://image.baidu.com/search/index?ct=201326592&cl=2&st=-1&lm=-1&nc=1&ie=utf-8&tn=baiduimage&ipn=r&rps=1&pv=&fm=rs2&word=%E5%BB%BA%E7%AD%91%E5%B7%A5%E4%BA%BA%E6%91%84%E5%BD%B1&oriquery=%E5%BB%BA%E7%AD%91%E5%B7%A5%E4%BA%BA&ofr=%E5%BB%BA%E7%AD%91%E5%B7%A5%E4%BA%BA'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser') #parser=解析器、分析器
    for img in soup.find_all('img', class_="preview"):
        target_url = 'http:' + img['src']
        filename = os.path.join('imgs', target_url.split('/')[-1])
        download(target_url, filename)
    print('%d / %d' % (i, end))

	#requests: 该库提供了http所有的基本请求方式：如
	#		r = requests.post("http://httpbin.org/post")
	#		r = requests.put("http://httpbin.org/put")
	#		r = requests.delete("http://httpbin.org/delete")
	#		r = requests.head("http://httpbin.org/get")
	#		r = requests.options("http://httpbin.org/get")
	
	#		payload = {'key1':'value1', 'key2':'value2'}
	#		r = requests.get("http://httpbin.org/get", param=payload)
	#		print r.url #http://httpbin.org/get?key1=value1&key2=value2 #r.text