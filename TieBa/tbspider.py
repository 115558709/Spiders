#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lxml import etree
from multiprocessing.dummy import Pool
import requests
import json
import sys
import random

class tieba_spider():
    headers = [
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]

    def Parse_Page(self,url):
        response=requests(url,headers=random.choice(self.headers))
        selector=etree.HTML(response.content)
        content_fields=selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
        item={}
        for content in content_fields:
            data_field=json.loads(content.xpath('@data-field')[0])
            author=data_field['author']['user_time']
            