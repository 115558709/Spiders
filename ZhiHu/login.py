import requests
from lxml import etree
from urllib import urlretrieve
import time

class Zhihu_Login(object):
    phone_num=''
    password=''

    def Get_captcha(self):
        urlretrieve('http://www.zhihu.com/captcha.gif?r=%d' % (time.time()*1000),'captcha.gif')
        return raw_input('captcha:')

    def Login(self):
        session=requests.session()

        headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'}
        login_url='https://www.zhihu.com/login/phone_num'

        _xsrf=etree.HTML(requests.get('https://www.zhihu.com/#signin',verify=False).text).xpath('/html/body/input/@value')[0]
        data={
            '_xsrf':_xsrf,
            'password':self.password,
            'remember_me':True,
            'phone_num':self.phone_num,
#            'captcha':self.Get_captcha()
        }

        res=session.post(login_url,data=data,headers=headers,verify=False)
        if '\u767b\u9646\u6210\u529f' in res.text:
            print "Successfully login in."
            return True
        else:
            print "Login in failed."
            return False

    def Get_name(self):
        headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36',
                 'Cookie':'_za=6a409267-0c05-4796-95ff-b2bc4009911a; q_c1=cdc71de1f741439c9a24c111519f9acf|1456831673000|1454160308000; _xsrf=6000d5e8ffcca48e926ab4e4d3151ff2; cap_id="MDg5MDA1MzYzZWU2NDMxN2IzM2EzNzZmMDM3ODRiOTA=|1457158907|d2bcc8050d77064ea44deef6d9ac812e083ab92a"; __utmt=1; __utma=51854390.1053717863.1457151745.1457151745.1457158068.2; __utmb=51854390.8.10.1457158068; __utmc=51854390; __utmz=51854390.1457158068.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.000--|2=registration_date=20160305=1^3=entry_date=20160130=1; z_c0="QUZBQWkzRXFrUWtYQUFBQVlRSlZUUTBJQWxlYjhIS0JTWXBPSmxOakVFLV92WnhjWGthT0d3PT0=|1457158925|4eed1222b3e04b3271a4d967057ebb688508c4dc"; unlock_ticket="QUZBQWkzRXFrUWtYQUFBQVlRSlZUUldDMmxhZWgzZU5mbkloYl8wM0ZfMkZTaFp4R0N4T2NRPT0=|1457158925|038cc2b758d3012aac6150ec3902aadc9e474d43"; n_c=1'}

        if self.Login():
            res=requests.get('https://www.zhihu.com/settings/profile',headers=headers,verify=False)
            selector=etree.HTML(res.text)
            print str(selector.xpath('//*[@class="top-nav-profile"]/a/@href')[0])
            homepage_url='https://www.zhihu.com'+str(selector.xpath('//*[@class="top-nav-profile"]/a/@href')[0])
            print homepage_url
            home_selector=etree.HTML(requests.get(homepage_url,headers=headers,verify=False).text)
            name=home_selector.xpath('//*[@class="title-section ellipsis"]/span/text()')[0]
            print name.encode('utf-8')

    def __init__(self):
        self.Get_name()


a=Zhihu_Login()