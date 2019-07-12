# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class Sqlite3Pipeline(object):
    def __init__(self,sqlite_file,sqlite_table):
        self.sqlite_file=sqlite_file
        self.sqlite_table=sqlite_table

    @classmethod
    def from_crawler1(cls, crawler):
        return cls(
            sqlite_file=crawler.settings.get('SQLITE_FILE'),
            sqlite_table=crawler.settings.get('SQLITE_TABLE','webonsite_onsiteorigin')
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file = crawler.settings.get('SQLITE_FILE'), # 从 settings.py 提取
            sqlite_table = crawler.settings.get('SQLITE_TABLE', 'items')
        )

    def open_spider(self,spider):
        self.connect=sqlite3.connect(self.sqlite_file)
        self.cursor=self.connect.cursor()

    def close_spider(self,spider):
        self.connect.close()

    def process_item(self,item,spider):
        item=dict(item)
        table_name=self.sqlite_table.get(spider.name,None) #get the database table name according to spider name
        if not table_name:
            spider.logger.error('Can not match the sqlite table for the spider {0}'.format(spider.name))
            return
        insert_sql='insert into {0}({1}) values({2})'.format(table_name,
                                                         ','.join(item.keys()),
                                                         ','.join(len(item.keys())*['?']))
        msg='item={2},\nsql string="{0} \n values={1}"'.format(insert_sql,item.values(),item)
        #print(msg)
        spider.logger.info(msg)
        values=[]
        for value in item.values(): #item.values is 2-d list, [[],[]], value=[]
            if len(value)>0:
                values.append(value[0])
            else: #For some fields , the value list is Null []
                values.append(None)
        spider.logger.info('values={0}'.format(values))
        try:
            self.cursor.execute(insert_sql,values)
            self.connect.commit()
        except Exception as e:
            spider.logger.error('error when insert item {0} : {1}'.format(item.get('property_id'),e))

        return item

