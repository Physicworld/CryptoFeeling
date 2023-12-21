import scrapy


class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    datetime = scrapy.Field()
    content = scrapy.Field()
    sentiment = scrapy.Field()
