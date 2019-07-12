import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Compose
from tutorial.items import Rent_Item
from scrapy_splash import SplashRequest
import datetime

class Rent_List_Spiler(scrapy.Spider):
    name='rent'
    #start_urls=['https://www.realestate.com.au/rent/in-seventeen+mile+rocks,+qld+4073/list-1']
    start_urls=['https://www.realestate.com.au/rent/in-riverhills+qld+4066/list-1']
    #start_urls = ['https://www.realestate.com.au/property-apartment-qld-sherwood-424755946']
    web_url='https://www.realestate.com.au'

    def parse(self,response):
        #yield SplashRequest(self.start_urls[0],self.parse_rent,endpoint='render.html',args={'wait':20,'timeout':90},)
        #return
        for href in response.css('.resultBody div.listingInfo div.buttons a.detailsButton::attr(href)'):
            detail_page=self.web_url+href.extract()
            self.logger.info('the url is = {0}'.format(detail_page))
            yield response.follow(href,callback=self.parse_rent)
            #below record 2018-09 -28 , because docker will exit , below splash can only get about 60 out of 300 records, so set this aside and five up the meidum rate data
            #yield SplashRequest(detail_page, self.parse_rent, #use splash to run the javascript to get the school , medium rate data
                                #endpoint='render.html',
                                #args={'wait': 20,'timeout':3600},)

        #next page
        for a in response.css('li.nextLink a'):
            yield response.follow(a,callback=self.parse)

    def parse_rent(self,response):
        loader=ItemLoader(item=Rent_Item(),response=response)
        loader.add_css('property_id','.property_id::text',TakeFirst(),re='Property No.\s(\d+)$')
        loader.add_value('crawl_date',datetime.date.today())
        loader.add_css('street_address','.street-address::text',TakeFirst())
        loader.add_css('suburb','.detail-address::text',Compose(lambda v:v[0],str.strip)) #['Oxyley','QLD','4074'] -> 'Oxyley'
        loader.add_css('post_code','.detail-address::text',Compose(lambda v:v[2],str.strip)) #['Oxyley','QLD','4074'] -> '4074'
        loader.add_css('bed','#listing_info > ul > li.property_info > dl > dd:nth-child(2)::text',TakeFirst())
        loader.add_css('bathroom','#listing_info > ul > li.property_info > dl > dd:nth-child(4)::text',TakeFirst())
        loader.add_css('car','#listing_info > ul > li.property_info > dl > dd:nth-child(6)::text',TakeFirst())
        loader.add_css('property_type','#listing_info > ul > li.property_info > span::text',TakeFirst())
        #loader.add_css('price','.priceText::text',TakeFirst(),re='\$(\d+)\s')
        #loader.add_css('price_des','.priceText::text',TakeFirst(),re='\$\d+\s(\w+)$')
        loader.add_css('price','.priceText::text',re='((\$?\s?[\d,]+)|(\$\s?[\d,]+\.00))')
        loader.add_css('price_des','.priceText::text',TakeFirst())
        loader.add_css('date_available','.available_date span::text',TakeFirst())
        loader.add_css('title','#description .title::text',TakeFirst())
        loader.add_css('description','#description .body::text',TakeFirst())
        loader.add_xpath('bond','//*[@id="features"]//li[text()="Bond:"]/span/text()',TakeFirst())
        loader.add_xpath('allowance','//li[@class="header"][contains(text(),"Allowances")]/following-sibling::li//text()')
        loader.add_xpath('indoor_feature','//li[@class="header"][contains(text(),"Indoor Features")]/following-sibling::li//text()')
        loader.add_xpath('outdoor_feature','//li[@class="header"][contains(text(),"Outdoor Features")]/following-sibling::li//text()')
        loader.add_xpath('other_feature','//li[@class="header"][contains(text(),"Other Features")]/following-sibling::li//text()')
        floor_plan_url=response.xpath('//*[@id="floorplans"]/ul/li/a/@href').extract_first() #/floorplan_new.ds?id=415840969&theme=rea.rent
        if floor_plan_url:
            loader.add_value('floorplan',response.urljoin(floor_plan_url)) #https://www.realestate.com.au/floorplan_new.ds?id=415840969&theme=rea.rent
        else:
            loader.add_value('floorplan','Not provided')
        #loader.add_xpath('school','//div[contains(text(),"Nearby schools")]/span[contains(@class,"is-selected")]//text()')
        loader.add_xpath('school','//*[@id="schoolInfo"]//text()')
        loader.add_xpath('median_rent','//*[@id="rpdataMedianPrice"]//span[@class="price"]/text()')
        loader.add_xpath('rental_yield','//*[@class="rentalYield"]//span[@class="rate"]/text()')
        loader.add_xpath('agency','//*[@class="listAgentName"]/text()',TakeFirst())
        loader.add_xpath('agent','//div[@class="bottomContent"]//*[@class="agentName"]/text()')
        loader.add_value('url',response.url)


        item=loader.load_item()


        return item