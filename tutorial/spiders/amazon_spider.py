import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Compose
from tutorial.items import OnsiteItem,OnsiteItemSqlite,AmazonProductItem
#from tutorial.items_amazon import AmazonProductItem
import datetime

class Amazon_Spiler(scrapy.Spider):
    name='amazon'
    start_urls=['https://www.amazon.com/b?node=18637582011&pf_rd_p=e7e982e4-29ff-4070-af4f-4f0cfa142b69&pf_rd_r=71R7HH7YQ8EKKD72RDXJ']

    def parse(self,response):
        for href in response.css('.a-link-normal::attr(href)'):
            #next_page=href.extract()
            #print('a_list='+next_page)
            yield response.follow(href,callback=self.parse_csv)

        for a in response.css('div.paginator li a'):
            title=a.css('a::attr(title)').extract_first()
            if title.startswith('Next'):
                yield response.follow(a,callback=self.parse)

    def parse_csv(self,response):
        print('respone url',response.url)
        loader=ItemLoader(item=AmazonProductItem(),response=response)
        loader.add_css('productTitle','#productTitle::text',MapCompose(str.strip))
        loader.add_css('acrCustomerReviewText','#acrCustomerReviewText::text')
        loader.add_css('priceblock_ourprice','#priceblock_ourprice::text',TakeFirst())
        item=loader.load_item()
        return item

    def parse_mr_sqlite(self,response):
        loader=ItemLoader(item=OnsiteItemSqlite(),response=response)
        loader.add_css('property_id','ul.amenities-detail li:nth-child(2)::text')
        loader.add_css('last_update','ul.amenities-detail li:nth-child(4)::text')
        loader.add_css('suburb','ul.amenities-detail li:nth-child(7) strong::text',MapCompose(str.strip))
        loader.add_css('agency','img.sidebarAgentLogo::attr(alt)',TakeFirst())
        loader.add_css('agent','div.pgl-agent-info h3 a::text',TakeFirst())
        loader.add_css('title','div.pgl-detail div.row div.col-sm-12 h1::text')
        loader.add_css('price','div.pgl-detail div.row div.col-sm-12 h2::text',TakeFirst())
        loader.add_css('income','#collapseOne ul li:nth-child(2)::text',TakeFirst())
        loader.add_css('unit_price','#collapseOne ul li:nth-child(3)::text',TakeFirst())
        loader.add_css('multiplier','#collapseOne ul li:nth-child(4)::text',re='\s(\d+[.]\d+)')
        loader.add_css('letting','#collapseTwo  li:nth-child(1)::text',re='\s(\d+).*')
        loader.add_css('owner_occupy','#collapseTwo  li:nth-child(2)::text',re='\s(\d+).*')
        loader.add_css('look_ups','#collapseTwo  li:nth-child(3)::text',re='\s(\d+).*')
        loader.add_css('outside_agents','#collapseTwo  li:nth-child(4)::text',re='\s(\d+).*')
        loader.add_css('total_unit','#collapseTwo  li:nth-child(5)::text',re='\s(\d+).*')
        loader.add_css('remuneration','#collapseThree  li:nth-child(1)::text',TakeFirst())
        loader.add_css('agreement_term','#collapseThree  li:nth-child(2)::text',MapCompose(str.strip),re='(\d+)')
        loader.add_css('agreement_remain','#collapseThree  li:nth-child(3)::text',MapCompose(str.strip),re='(\d+)')
        loader.add_css('agreement_age','#collapseThree  li:nth-child(4)::text',MapCompose(str.strip),re='(\d+)')
        loader.add_css('office_hour','#collapseThree  li:nth-child(5)::text')
        loader.add_css('complex_feature','#collapseThree  li:nth-child(6)::text')
        loader.add_css('manager_bed','#collapseFour  li:nth-child(1)::text',Compose(lambda v:v[1],str.strip,stop_on_none=True))
        loader.add_css('manager_bathroom','#collapseFour  li:nth-child(1)::text',Compose(lambda v:v[2],str.strip,stop_on_none=True))
        loader.add_css('manager_car','#collapseFour  li:nth-child(3)::text')
        loader.add_css('office','#collapseFour  li:nth-child(4)::text',re='\s(\d+).*')
        loader.add_css('pets','#collapseFour  li:nth-child(5)::text',MapCompose(str.strip))
        loader.add_css('unit_feature','#collapseFour  li:nth-child(6)::text')
        loader.add_css('description','div.pgl-detail div.row div.col-sm-12 p::text')
        #loader.add_value('description','tmp description')
        loader.add_value('url',response.url)
        loader.add_value('crawl_date',datetime.date.today())
        price=loader.get_output_value('price')[0]
        #self.logger.info('get out_put price={0}'.format(price))
        unit_price=loader.get_output_value('unit_price')[0]

        try:
            if price !=0:
                loader.add_value('unit_percentage',round(unit_price/price,2))
        except Exception as e:
            print('error when calculate unit pecentage: {0}'.format(e))
            loader.add_value('unit_percentage', 0)

        try:
            income=loader.get_output_value('income')[0]
            remuneration=loader.get_output_value('remuneration')[0]
            total_unit=loader.get_output_value('total_unit')[0]
            letting=loader.get_output_value('letting')[0]
            if total_unit!=0:
                loader.add_value('wage_per_unit',round(remuneration/total_unit,2))
            else:
                loader.add_value('wage_per_unit', 0)
            if letting!=0:
                loader.add_value('income_per_letting',round((income-remuneration)/letting,2))
            else:
                loader.add_value('income_per_letting',0)
        except Exception as e:
            print('error when calculate income pecentage: {0}'.format(e))
            loader.add_value('wage_per_unit', 0)
            loader.add_value('income_per_letting', 0)

        item=loader.load_item()

        return item