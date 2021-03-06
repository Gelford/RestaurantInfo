# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import codecs
import json


class WebcrawlerScrapyPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],  
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8', #for chinese characters
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  
        return cls(dbpool)  

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item) 
        query.addErrback(self._handle_error, item, spider) 
        return item

    def _conditional_insert(self, tx, item):
        sql = "insert into foodshops(shopname,shoplevel,shopurl,commentnum,avgcost,taste,envi,service,foodtype,loc,address,city) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item['shopname'], item['shoplevel'], item['shopurl'], item['commentnum'],item['avgcost'],item['taste'],item['envi'],item['service'],item['foodtype'],item['loc'],item['address'],item['city'])
        tx.execute(sql, params)


    def _handle_error(self, failue, item, spider):
        print failue

