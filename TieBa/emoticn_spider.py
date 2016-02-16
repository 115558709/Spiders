from urllib import urlretrieve
import os

class emoticon_spider():
    url='http://static.tieba.baidu.com/tb/editor/images/client/image_emoticon%d.png'
    emo_num=1
    image_path=("tieba_emotion/")

    def Get_Image(self):
        url=self.url % self.emo_num
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
        while(self.emo_num<51):
            self.Get_Image()
            self.emo_num+=1

sp=emoticon_spider()