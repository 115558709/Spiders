# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Good(Item):
    rank=Field()
    title=Field()
    price=Field()
    turnover_index=Field()
    top_id=Field()
    type_id=Field()

