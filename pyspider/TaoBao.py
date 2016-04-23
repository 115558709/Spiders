#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-04-21 18:18:34
# Project: demo

from pyspider.libs.base_handler import *
import os
import re
import json


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'GoogleBot',
        }
    }
    
    def __init__(self):
        self.path=("/home/wqlin/淘宝/")
        self.base_url='https://top.taobao.com/index.php?spm=a1z5i.1.2.1.hUTg2J&topId=HOME'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.base_url,callback=self.index_page,fetch_type='js')

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        print response.doc('#TR_FS')
        self.crawl(response.doc('#TR_FS').attr.href,callback=self.detail_page,fetch_type='js')
        self.crawl(response.doc('#TR_SM').attr.href,callback=self.detail_page,fetch_type='js')
        self.crawl(response.doc('#TR_HZP').attr.href,callback=self.detail_page,fetch_type='js')
        self.crawl(response.doc('#TR_MY').attr.href,callback=self.detail_page,fetch_type='js')
        self.crawl(response.doc('#TR_SP').attr.href,callback=self.detail_page,fetch_type='js')
        self.crawl(response.doc('#TR_WT').attr.href,callback=self.detail_page,fetch_type='js')
        self.crawl(response.doc('#TR_JJ').attr.href,callback=self.detail_page,fetch_type='js')
        self.crawl(response.doc('#TR_ZH').attr.href,callback=self.detail_page,fetch_type='js')
            
    @config(priority=2)
    def detail_page(self,response):
        for each in response.doc('.block-body a').items():
            self.crawl(each.attr.href,
                       callback=self.process_page,
                       fetch_type='js')
            
    @config(priority=3)
    def process_page(self,response):
        for each in response.doc('.switch-row a').items():
            if re.match(r'.*rank=sale&type=hot.*',each.attr.href):
                self.crawl(each.attr.href,callback=self.result_page,fetch_type='js')
        
        
    @config(priority=3)
    def result_page(self,response):
        dir_attr=response.doc('li > .selected').text()
        if '/' in dir_attr:
            dir_tuple=dir_attr.split('/')
            dir_attr=''
            for d in dir_tuple:
                dir_attr+=d+'|'
        dir_path=self.path+dir_attr+'/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        item_name=[]
        item_sale=[]
        for each in response.doc('.param-item-selected').items():
            title=each.text()
        #print title
        if '/' in title:
            title_tuple=title.split('/')
            title=''
            for t in title_tuple:
                title+=t+'|'
        for each in response.doc('.col2 a').items():
            item_name.append(each.text())
        for each in response.doc('div > .num').items():
            item_sale.append(each.text())
        with open(dir_path+title+'.txt','a') as f:
            for k,v in zip(item_name,item_sale):
                item_dict={}
                item_dict[k]=v
                f.write(str(item_dict).decode('unicode-escape')+'\n')
        with open(dir_path+'总集合.txt','a') as f:
            f.write(title+'\n')
            for k,v in zip(item_name,item_sale):
                item_dict={}
                item_dict[k]=v
                f.write(str(item_dict).decode('unicode-escape')+'\n')
            f.write('\n\n\n')