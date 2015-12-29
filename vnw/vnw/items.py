# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class PyjobItem(Item):
    name = Field()
    company = Field()
    address = Field()
    province = Field()
    wage = Field()
    welfare = Field()
    skill = Field()
    work = Field()
    specialize = Field()
    information = Field()
    contact = Field()
    size = Field()
    logo = Field()
    pass
