import scrapy

class Quotes_Spider(scrapy.Spider):
    name='quotes'


    def start_requests(self):
        #urls=['http://quotes.toscrape.com/page/1/']
        #for url in urls:
        #    yield scrapy.Request(url=url,callback=self.parse)
        url='http://quotes.toscrape.com/'
        #tag=getattr(self,'tag',None)
        if self.tag:
            url=url+'tag/'+self.tag
        yield scrapy.Request(url=url,callback=self.parse)


    #start_urls=['http://quotes.toscrape.com/page/1/']


    def parse(self, response):
        '''
        page=response.url.split('/')[-2]
        filename='quotes-{0}.html'.format(page)
        with open(filename,'wb') as f:
            f.write(response.body)
        self.log('saved file {0}'.format(filename))
        '''
        for quote in response.css('div.quote'):
            yield{
                'text':quote.css('span.text::text').extract_first(),
                'author':quote.css('small.author::text')[0].extract(),
                'tags':quote.css('div.tags a.tag::text').extract(),
            }
        #next_page=response.css('li.next a::attr(href)').extract_first()
        #if next_page is not None:
            #next_page=response.urljoin(next_page)
            #yield scrapy.Request(next_page,callback=self.parse)
            #yield response.follow(next_page,callback=self.parse)
        #for href in response.css('li.next a::attr(href)'):
            #yield response.follow(href,callback=self.parse)
        #for a in response.css('li.next a'):
            #yield response.follow(a,callback=self.parse)
        yield response.follow(response.css('li.next a')[0],callback=self.parse)
