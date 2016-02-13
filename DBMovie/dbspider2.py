from urllib2 import urlopen,Request
from bs4 import BeautifulSoup
import random
import re
from urlparse import urljoin
import os
from types import NoneType

class douban_Movie_spider():
    url="http://movie.douban.com/top250?start=&filter="
    page_num=0
    top_num=1
    rule=re.compile("^(http://movie.douban.com/subject)(.)*(/)$")
    links_set=set()
    headers = [
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]
    file_path="Movie/"

    def Parse_Page(self):
        request=Request(urljoin(self.url,"top250?start="+str(self.page_num*25)+"&filter="),headers=random.choice(self.headers))
        response=urlopen(request)
        page_bsObj=BeautifulSoup(response,"lxml")
        for link in page_bsObj.find_all("a",href=self.rule):
            if 'href' in link.attrs:
                if link.attrs['href'] not in self.links_set:
                    self.links_set.add(link.attrs['href'])
                    self.Parse_Movie(link.attrs['href'])
                    self.top_num+=1


    def Parse_Movie(self,link):
        try:
            print("Top "+str(self.top_num)+" link is: "+link)
            request=Request(link,headers=random.choice(self.headers))
            response=urlopen(request)
            movie_bsObj=BeautifulSoup(response,"lxml")
            title=movie_bsObj.h1
            movie_info=movie_bsObj.find("div",id="info")
            h2=movie_bsObj.h2
            movie_intro=movie_bsObj.find("span",{"class":"all hidden"})
            if isinstance(movie_intro,NoneType)==True:
                movie_intro=movie_bsObj.find("span",{"property":"v:summary"})
            with open(self.file_path+"Top "+str(self.top_num)+".txt",'w') as f:
                f.write(title.get_text().encode('utf-8'))
                f.write(movie_info.get_text().encode('utf-8')+'\n')
                f.write(h2.get_text().encode('utf-8')+'\n')
                f.write(movie_intro.get_text().encode('utf-8').strip())
        except Exception as e:
            if hasattr(e,"reason"):
                print(e.reason)

    def __init__(self):
        if not os.path.exists(self.file_path):
            os.mkdir(self.file_path)
        while(self.page_num<=9):
            self.Parse_Page()
            self.page_num+=1

sp=douban_Movie_spider()