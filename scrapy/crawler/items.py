# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Good(Item):
    title=Field()
    price=Field()
    points=Field()
    type=Field()

