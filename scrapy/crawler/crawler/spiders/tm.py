# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy import Request
from utils import extract,extract_one
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

class JDSpider(Spider):
    name='tm'
    allowed_domains=['tmall.com']
    start_urls=['http://www.tmall.com/']
    #https://list.tmall.com/search_product.htm?spm=a221t.1476805.2109261262.3.OkzdaD&abbucket=&cat=50025135&shopType=any&sort=s&acm=lb-zebra-7419-257470.1003.8.405203&style=g&aldid=155791&search_condition=48&prop=148380063%3A852486590&active=1&from=sn_1_prop&abtest=&scm=1003.8.lb-zebra-7419-257470.ITEM_14477963479932_405203&pos=3
    normal_url_pattern=[r'.*list\.tmall\.com/.*']
    normal_url_extractor=LxmlLinkExtractor(allow=normal_url_pattern)
    needed_url_pattern=['r.*//list\.jd\.com/list\.html?cat.*sort=sort_totalsale.*']
    needed_url_extractor=LxmlLinkExtractor(allow=needed_url_pattern)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,callback=self.parse,args={
                'wait':2.5,'html':1,})

    def parse(self,response):
        hxs=Selector(response)
        url_group=extract(hxs,"//div[@id='content']//div[@class='nav-con j_tabPannel category-tab-pannel']/ul[@class='normal-nav clearfix']//a/@href")
        for url in url_group:
            url='https:'+url
            yield SplashRequest(url,callback=self.extract_url,args={'wait':2.5,'html':1,})

    def extract_url(self,response):
        for link in self.normal_url_extractor.extract_links(response):
            yield SplashRequest(link.url,callback=self.parse_url,args={'wait':2.5,'html':1,})

    def parse_url(self,response):
        for link in self.needed_url_extractor.extract_links(response):
            print url
            url='http:'+link.url
