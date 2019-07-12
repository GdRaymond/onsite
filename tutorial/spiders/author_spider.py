import scrapy
from tutorial.items import AuthorItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose

class Author_Spider(scrapy.Spider):

    name='authors'
    start_urls=['http://quotes.toscrape.com']

    def parse(self, response):
        for a in response.css('.author + a'):
            yield response.follow(a, callback=self.parse_author_loader)

        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)

    '''
    def parse_author(self,response):
        def extra_with_css(query):
            return response.css(query).extract_first().strip()

        yield{
            'name': extra_with_css('h3.author-title::text'),
            'birthday': extra_with_css('.author-born-date::text'),
            'bio': extra_with_css('.author-description::text'),
        }
    '''
    def parse_author_loader(self,response):
        loader=ItemLoader(item=AuthorItem(),response=response)
        loader.add_css('name','h3.author-title::text',MapCompose(str.strip))
        loader.add_css('birthday','.author-born-date::text',MapCompose(str.strip))
        loader.add_css('bio','.author-description::text')
        return loader.load_item()
