from urllib2 import urlopen
from bs4 import BeautifulSoup
from urlparse import urljoin
import datetime

class DBMovieSpider():
    url="http://movie.douban.com/top250?start=&filter="
    page_num=0
    top_num=1

    def Parse_Page(self):
        response=urlopen(urljoin(self.url,'top250?start='+str(self.page_num*25)+'&filter='))
        page_bsObj=BeautifulSoup(response,"lxml")
        try:
            movie_items=page_bsObj.find_all("span",{"class":"title"})
            with open('Movie Top250.txt','a') as f:
                for i,item in enumerate(movie_items):
                        if movie_items[i].get_text().encode('utf-8').find('/')!=-1:
                            f.write(movie_items[i].get_text().encode('utf-8')+'\n')
                        else:
                            try:
                                movie_items[i+1].get_text().encode('utf-8')
                                if movie_items[i+1].get_text().encode('utf-8').find('/')==-1:
                                    f.write("Top "+str(self.top_num)+": "+movie_items[i].get_text().encode('utf-8')+'\n')
                                else:
                                    f.write("Top "+str(self.top_num)+": "+movie_items[i].get_text().encode('utf-8'))
                            except Exception,e:
                                f.write("Top "+str(self.top_num)+": "+movie_items[i].get_text().encode('utf-8')+'\n')
                            finally:
                                self.top_num+=1
        except Exception as e:
            if hasattr(e,"reason"):
                print(e.reason)

    def __init__(self):
        with open('Movie Top250.txt','a') as f:
            f.write("Update time: "+str(datetime.datetime.now())+'\n')
        while(self.page_num<=9):
            self.Parse_Page()
            self.page_num+=1

sp=DBMovieSpider()