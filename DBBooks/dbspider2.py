# -*- coding:utf-8 -*-
from urllib2 import urlopen,Request
from bs4 import BeautifulSoup
from urlparse import urljoin
import datetime
import os
import random

class DBBooks_Spider():
    url="http://book.douban.com/top250?start="
    page_num=0
    top_num=1
    headers=[
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]
    file_path=("Books/")

    def Parse_Page(self):
        page_request=Request(urljoin(self.url,'top250?start='+str(self.page_num*25)),headers=random.choice(self.headers))
        response=urlopen(page_request)
        page_bsObj=BeautifulSoup(response,"lxml")
        books_items=page_bsObj.find_all("a")
        for item in books_items:
            if 'title' in item.attrs:
                self.Parse_Book(item.attrs['href'])
                self.top_num+=1


    def Parse_Book(self,book_url):
        print("book_url is: "+book_url)
        try:
            book_request=Request(book_url,headers=random.choice(self.headers))
            response=urlopen(book_request)
            book_bsObj=BeautifulSoup(response,"lxml")
            book_title=book_bsObj.h1
            book_info=book_bsObj.find("div",{"id":"info"})
            intro=book_bsObj.find_all("div",{"class":"intro"})
            if intro[0].get_text().encode('utf-8').find('展开全部')!=-1:
                book_intro=intro[1]
                if intro[2].get_text().encode('utf-8').find('展开全部')!=-1:
                    author_intro=intro[3]
                else:
                    author_intro=intro[2]
            else:
                book_intro=intro[0]
                if intro[1].get_text().encode('utf-8').find('展开全部')!=-1:
                    author_intro=intro[2]
                else:
                    author_intro=intro[1]
            with open(self.file_path+'Top'+str(self.top_num)+'.txt','w') as f:
                f.write(book_title.get_text().encode('utf-8').strip()+'\n')
                info_text=book_info.get_text().encode('utf-8').split(' ')
                for info in info_text:
                    if info!='\n' and info!='':
                        f.write(info.strip())
                f.write("\n\n内容简介: ")
                f.write(book_intro.get_text().encode('utf-8'))
                f.write("\n\n作者简介: ")
                f.write(author_intro.get_text().encode('utf-8'))
        except Exception as e:
            if hasattr(e,"reason"):
                print("Reason: "+e.reason)

    def __init__(self):
        if not os.path.exists(self.file_path):
            os.mkdir(self.file_path)
        while(self.page_num<=9):
            self.Parse_Page()
            self.page_num+=1

sp=DBBooks_Spider()