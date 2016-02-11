from urllib2 import urlopen
from bs4 import BeautifulSoup
from urlparse import urljoin
import datetime

class DBBooks_Spider():
    url="http://book.douban.com/top250?start="
    page_num=0
    top_num=1

    def Parse_Page(self):
        response=urlopen(urljoin(self.url,'top250?start='+str(self.page_num*25)))
        page_bsObj=BeautifulSoup(response,"lxml")
        books_items=page_bsObj.find_all("a")
        with open('Books Top250.txt','a') as f:
            for item in books_items:
                if 'title' in item.attrs:
                    f.write("Top "+str(self.top_num)+": "+item.attrs['title'].encode('utf-8')+'\n')
                    self.top_num+=1

    def __init__(self):
        with open('Books Top250.txt','a') as f:
            f.write("Update time: "+str(datetime.datetime.now())+'\n')
        while(self.page_num<=9):
            self.Parse_Page()
            self.page_num+=1

sp=DBBooks_Spider()