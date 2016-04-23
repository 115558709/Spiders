import sys

reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.exceptions import DropItem

from crawler.items import Good
from crawler.db import good_Table

class CheckPipeline(object):
    def process_item(self,item,spider):
        for key in item:
            if item[key]==None:
                raise DropItem('%s is missing %s' % (item,key))
        return item

class MySQLPipeline(object):
    def __init__(self,host,username,password,db):
        self.host = host
        self.username = username
        self.password = password
        self.db = db

    @measure('MySQLPipeline')
    def process_item(self,item,spider):
        self.table.insert(item['title'],item['price'],item['points'],item['type'])
        return item

    @classmethod
    def from_settings(cls,settings):
        host=settings['MYSQL_HOST']
        username=settings['MYSQL_USERNAME']
        
    
        

    
