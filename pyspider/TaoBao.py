#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-04-21 18:18:34
# Project: demo

from pyspider.libs.base_handler import *
import os

class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'GoogleBot',
        }
    }

    def __init__(self):
        self.path=("/home/wqlin/TaoBao/")
        self.base_url='https://top.etao.com/index.php?spm=a1z5i.2.2.2.lCYrOD&topId=TR_FS&leafId=50010850'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.base_url,callback=self.index_page,fetch_type='js')

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('#TR_SM').items():
            print each.attr.href
            self.crawl(each.attr.href,callback=self.detail_page,
                    fetch_type='js')
            
    @config(priority=2)
    def detail_page(self,response):
        for each in response.doc('.block-body a').items():
            self.crawl(each.attr.href,
                       callback=self.result_page,
                       fetch_type='js')
        
    @config(priority=3)
    def result_page(self,response):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        item_name=[]
        item_num=[]
        for each in response.doc('.param-item-selected').items():
            title=each.text()
        for each in response.doc('.col2 a').items():
            item_name.append(each.text())
        for each in response.doc('div > .num').items():
            item_num.append(each.text())
        for j,k in zip(item_name,item_num):
            print j,'  ',k,'\n'
        with open(self.path+title+'.json','a') as f:
            for j,k in zip(item_name,item_num):
                f.write(j+'  '+k+'\n')