#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pyspider.libs.base_handler import *
import re

class Handler(BaseHandler):
    crawl_config={
        'headers':{'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'}
    }

    def __init__(self):
        self.url='http://www.imdb.com/search/title?count=100&ref_=nv_ch_mm_1&sort=user_rating&start=%d&title_type=feature,tv_series,tv_movie'

    @every(minutes=24*60)
    def on_start(self):
        for i in range(1,536000,100):
            url=self.url % i
            self.crawl(url,callback=self.index_page)

    @config(priority=1)
    def index_page(self,response):
        for each in response.doc('a[href^="http"]').items():
            if re.match(r"http://www\.imdb\.com/title/tt\d+/$",each.attr.href):
                self.crawl(each.attr.href,callback=self.detail_page)

    @config(priority=2)
    def detail_page(self,response):
        return {
            "url":response.url,
            "title":response.doc('#main > table > tbody > tr:nth-child(2) > td.title > a').text(),
            "rating":response.doc('[itemprop="ratingValue"]').text()
            }
