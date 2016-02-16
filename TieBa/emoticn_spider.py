from urllib import urlretrieve
import os
from multiprocessing.dummy import Pool

class emoticon_spider():
    url='http://static.tieba.baidu.com/tb/editor/images/client/image_emoticon%d.png'
    image_path=("tieba_emotion/")

    def Get_Image(self,url):
        print url
        try:
            image_title=url.split('/')[-1]
            urlretrieve(url,filename=self.image_path+image_title)
        except Exception as e:
            if hasattr(e,'reason'):
                print(e.reason)

    def __init__(self):
        if not os.path.exists(self.image_path):
            os.mkdir(self.image_path)
        urls=[]
        for i in range(1,51):
            url=url % i
            urls.append(url)

        pool=Pool(4)
        thread=pool.map(self.Get_Image,urls)
        pool.close()
        pool.join()

sp=emoticon_spider()