# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy,re
from scrapy.loader.processors import MapCompose,Compose


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AuthorItem(scrapy.Item):
    name=scrapy.Field()
    birthday=scrapy.Field()
    bio=scrapy.Field(
        input_processor=MapCompose(str.strip)
    )

class TakeSecond(object):

    def __call__(self, values):
        for i in range(len(values)):
            if i == 1 :
                if values[i] is not None and values[i] != '':
                    return values[i]

def convert_money(value):
    value=value.strip().strip(',')
    import re
    #pattern=(r'\$\s?[\d,]+$')
    #m=re.findall(pattern,value)
    pattern=(r'((\$\s?[\d,]+)|(\$\s?[\d,]+\.00))')
    m=re.search(pattern,value)
    if m:
        print('matched m={0}'.format(m))
        #return m[-1].strip('$').strip(',').strip().replace(',','') #when using re.findall, get last item
        return m.group(1).strip('$').strip(',').strip().replace(',','')
    else:
        print('Not matched value={0}'.format(value))
        return value

def convert_income(value):
    pattern=(r'\$\s?[\d,]+\s')
    m=re.findall(pattern,value)
    if m:
        print('matched m={0}'.format(m))
        return m[-1].strip('$').strip(',').strip().replace(',','')
    else:
        print('Not matched value={0}'.format(value))
        return value

def get_agency(value):
    pattern=(r'.*for:(.*)$')
    m=re.match(pattern,value)
    print('agency value={0}'.format(value))
    if m:
        print('  m.group(1)={0}'.format(m.group(1)))
        return m.group(1)
    else:
        return value

def convert_to_float(value):
    try:
        result=float(value)
    except Exception as e:
        print('error when convert {0} to float: {1}'.format(value,e))
        result=0
    return result

def convert_to_int(value):
    try:
        result=int(float(value))
    except Exception as e:
        print('error when convert {0} to int: {1}'.format(value, e))
        result = 0
    return result

def strip_comma(value):
    return value.strip().strip(',')


class AmazonProductItem(scrapy.Item):
    productTitle=scrapy.Field()
    acrCustomerReviewText=scrapy.Field()
    priceblock_ourprice=scrapy.Field()


class OnsiteItemSqlite(scrapy.Item):
    suburb=scrapy.Field(
        input_processor=MapCompose(strip_comma)
    )
    price=scrapy.Field(
        input_processor=MapCompose(convert_money),
        output_processor=MapCompose(convert_to_float)
    )
    unit_price=scrapy.Field(
        input_processor=MapCompose(convert_money),
        output_processor = MapCompose(convert_to_float)
    )
    unit_percentage=scrapy.Field()
    income=scrapy.Field(
        input_processor=MapCompose(convert_income),
        output_processor = MapCompose(convert_to_float)
    )
    remuneration=scrapy.Field(
        input_processor=MapCompose(convert_money),
        output_processor = MapCompose(convert_to_float)

    )
    multiplier=scrapy.Field(
        output_processor=MapCompose(convert_to_float)

    )
    agreement_term=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    agreement_remain=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    agreement_age=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    total_unit=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    wage_per_unit=scrapy.Field(
        output_processor=MapCompose(convert_to_float)
    )
    owner_occupy=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    letting=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    income_per_letting=scrapy.Field(
        output_processor=MapCompose(convert_to_float)
    )
    look_ups=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    outside_agents=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    manager_bed=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    manager_bathroom=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    manager_car=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    office=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    office_hour=scrapy.Field()
    agency=scrapy.Field(
        input_processor=MapCompose(get_agency)
    )
    agent=scrapy.Field()
    complex_feature=scrapy.Field()
    url=scrapy.Field()
    title=scrapy.Field()
    description=scrapy.Field()
    unit_feature=scrapy.Field()
    pets=scrapy.Field()
    last_update=scrapy.Field()
    property_id=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    crawl_date=scrapy.Field()

class Rent_Item(scrapy.Item):
    property_id=scrapy.Field(
        output_processor=MapCompose(convert_to_int)
    )
    crawl_date=scrapy.Field()
    street_address=scrapy.Field()
    suburb=scrapy.Field()
    post_code=scrapy.Field()
    bed=scrapy.Field(
        output_processor=MapCompose(convert_to_int))
    bathroom=scrapy.Field(
        output_processor=MapCompose(convert_to_int))
    car=scrapy.Field(
        output_processor=MapCompose(convert_to_int))
    property_type=scrapy.Field()
    price=scrapy.Field(
        input_processor=MapCompose(convert_money),
        output_processor=MapCompose(convert_to_float)
    )
    price_des=scrapy.Field()
    date_available=scrapy.Field()
    title=scrapy.Field()
    description=scrapy.Field()
    bond=scrapy.Field(
        input_processor=MapCompose(convert_money),
        output_processor=MapCompose(convert_to_float)
    )
    allowance = scrapy.Field()
    indoor_feature = scrapy.Field()
    outdoor_feature = scrapy.Field()
    other_feature = scrapy.Field()
    floorplan = scrapy.Field()
    school = scrapy.Field()
    median_rent=scrapy.Field()
    rental_yield=scrapy.Field()
    agency=scrapy.Field()
    agent=scrapy.Field()
    url=scrapy.Field()


