import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Compose
from tutorial.items import OnsiteItem,OnsiteItemSqlite
import datetime

class Onsite_Spiler(scrapy.Spider):
    name='onsite'
    start_urls=['https://www.theonsitemanager.com.au/management-rights/permanent-management-rights/4000%2c+qld%2c+4000?search[proximity]=0.30']

    def parse(self,response):
        for href in response.css('.pgl-property  a::attr(href)'):
            #next_page=href.extract()
            #print('a_list='+next_page)
            yield response.follow(href,callback=self.parse_mr_sqlite)

        for a in response.css('div.paginator li a'):
            title=a.css('a::attr(title)').extract_first()
            if title.startswith('Next'):
                yield response.follow(a,callback=self.parse)

    def parse_mr(self,response):
        loader=ItemLoader(item=OnsiteItem(),response=response)
        loader.add_css('z6_property_id','ul.amenities-detail li:nth-child(2)::text')
        loader.add_css('z5_last_update','ul.amenities-detail li:nth-child(4)::text')
        loader.add_css('a0_address','ul.amenities-detail li:nth-child(7) strong::text',MapCompose(str.strip))
        loader.add_css('w0_agency','img.sidebarAgentLogo::attr(alt)',TakeFirst())
        loader.add_css('x0_agent','div.pgl-agent-info h3 a::text')
        loader.add_css('z1_title','div.pgl-detail div.row div.col-sm-12 h1::text')
        loader.add_css('b0_price','div.pgl-detail div.row div.col-sm-12 h2::text',TakeFirst())
        loader.add_css('e0_income','#collapseOne ul li:nth-child(2)::text',TakeFirst())
        loader.add_css('c0_unit_price','#collapseOne ul li:nth-child(3)::text',TakeFirst())
        loader.add_css('g0_multiplier','#collapseOne ul li:nth-child(4)::text',re='\s(\d+[.]\d+)')
        loader.add_css('n0_letting','#collapseTwo  li:nth-child(1)::text',re='\s(\d+).*')
        loader.add_css('m0_owner_occupy','#collapseTwo  li:nth-child(2)::text',re='\s(\d+).*')
        loader.add_css('p0_look_ups','#collapseTwo  li:nth-child(3)::text',re='\s(\d+).*')
        loader.add_css('q0_outside_agents','#collapseTwo  li:nth-child(4)::text',re='\s(\d+).*')
        loader.add_css('k0_total_unit','#collapseTwo  li:nth-child(5)::text',re='\s(\d+).*')
        loader.add_css('f0_remuneration','#collapseThree  li:nth-child(1)::text',TakeFirst())
        loader.add_css('h0_agreement_term','#collapseThree  li:nth-child(2)::text',MapCompose(str.strip))
        loader.add_css('i0_agreement_remaining','#collapseThree  li:nth-child(3)::text',MapCompose(str.strip))
        loader.add_css('j0_agreement_age','#collapseThree  li:nth-child(4)::text',MapCompose(str.strip))
        loader.add_css('v0_office_hour','#collapseThree  li:nth-child(5)::text')
        loader.add_css('y0_complex_fetures','#collapseThree  li:nth-child(6)::text')
        loader.add_css('r0_manager_bed','#collapseFour  li:nth-child(1)::text',Compose(lambda v:v[1],str.strip,stop_on_none=True))
        loader.add_css('s0_manager_bathroom','#collapseFour  li:nth-child(1)::text',Compose(lambda v:v[2],str.strip,stop_on_none=True))
        loader.add_css('t0_manager_car','#collapseFour  li:nth-child(3)::text')
        loader.add_css('u0_office','#collapseFour  li:nth-child(4)::text',re='\s(\d+).*')
        loader.add_css('z4_pets','#collapseFour  li:nth-child(5)::text',MapCompose(str.strip))
        loader.add_css('z3_unit_feature','#collapseFour  li:nth-child(6)::text')
        loader.add_css('z2_description','div.pgl-detail div.row div.col-sm-12 p::text')
        loader.add_value('z0_url',response.url)
        item=loader.load_item()
        print('item={0}'.format(item))
        unit_price=item['c0_unit_price'][0]
        price=item['b0_price'][0]
        try:
            price=int(float(price))
            unit_price=int(float(unit_price))
            if price !=0:
                item['d0_unitPercent']=round(unit_price/price,2)
        except Exception as e:
            print('error when calculate unit pecentage: {0}'.format(e))
            item['d0_unitPercent']  = 0

        try:
            income=int(float(item['e0_income'][0]))
            remuneration=int(float(item['f0_remuneration'][0]))
            total_unit=int(float(item['k0_total_unit'][0]))
            letting=int(float(item['n0_letting'][0]))
            if total_unit!=0:
                item['l0_rePerUnit']=round(remuneration/total_unit,2)
            else:
                item['l0_rePerUnit'] = 0
            if letting!=0:
                item['o0_iPerRent']=round((income-remuneration)/letting,2)
            else:
                item['o0_iPerRent'] =0
        except Exception as e:
            print('error when calculate income pecetage: {0}'.format(e))
            item['l0_rePerUnit'] = 0
            item['o0_iPerRent'] = 0

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