#encoding:utf-8
from icrawler.examples import GoogleImageCrawler
from icrawler.examples import BingImageCrawler
from icrawler.examples import BaiduImageCrawler

baidu_crawler1 = BaiduImageCrawler('picture')
baidu_crawler1.crawl(keyword='纯色背景图', offset=0, max_num=3000,
                    feeder_thr_num=1, parser_thr_num=1, downloader_thr_num=4,
                    min_size=None, max_size=None)
'''baidu_crawler2 = BaiduImageCrawler('constructionTools')
baidu_crawler2.crawl(keyword='建筑工具', offset=0, max_num=1000,
                    feeder_thr_num=1, parser_thr_num=1, downloader_thr_num=4,
                    min_size=None, max_size=None)
baidu_crawler3 = BaiduImageCrawler('engineeringVehicle')
baidu_crawler3.crawl(keyword='工程车辆', offset=0, max_num=1000,
                    feeder_thr_num=1, parser_thr_num=1, downloader_thr_num=4,
                    min_size=None, max_size=None)
baidu_crawler3 = BaiduImageCrawler('scaffold')
baidu_crawler3.crawl(keyword='脚手架', offset=0, max_num=1000,
                    feeder_thr_num=1, parser_thr_num=1, downloader_thr_num=4,
                    min_size=None, max_size=None)'''
