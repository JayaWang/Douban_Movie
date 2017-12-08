# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from With_DB import Mysql_DB
from items import DoubanJPItem, DoubanHTItem, DoubanDPItem

class DoubanCrawlPipeline(object):
    def __init__(self):
        self.db = Mysql_DB()

    def process_item(self, item, spider):
        if isinstance(item, DoubanDPItem):
            try:
                sql = """insert into DoubanDP (Uname, Star, DPtime, Liked, Content) VALUES ("%s", "%s", "%s", "%s", "%s")"""%(item["Uname"].encode('utf-8', 'ignore'), item["Star"].encode('utf-8', 'ignore'), item["DPtime"].encode('utf-8', 'ignore'), item["Liked"].encode('utf-8', 'ignore'), item["Content"].encode('utf-8', 'ignore'))
                self.db.Insert_MySQL(sql)
            except Exception as e:
                print '插入DP表错误' + str(e)
        if isinstance(item, DoubanHTItem):
            if item['sign'] == 'OUT':
                try:
                    sql = """insert into DoubanHTOUT (sign, HT_id, title, author, HT_href, reply, HTtime, Content) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")"""%(item['sign'].encode('utf-8', 'ignore'), item['HT_id'].encode('utf-8', 'ignore'), item['title'].encode('utf-8', 'ignore'), item['author'].encode('utf-8', 'ignore'), item['HT_href'].encode('utf-8', 'ignore'), item['reply'].encode('utf-8', 'ignore'), item['HTtime'].encode('utf-8', 'ignore'), item['Content'].encode('utf-8', 'ignore'))
                    self.db.Insert_MySQL(sql)
                except Exception as e:
                    print '插入HTOUT错误' + str(e)
            if item['sign'] == 'INSIDE':
                try:
                    sql = """insert into DoubanHTINSIDE (sign, HT_id, Rname, Rtime, Rcontent, Rliked) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")"""%(item['sign'].encode('utf-8', 'ignore'), item['HT_id'].encode('utf-8', 'ignore'), item['Rname'].encode('utf-8', 'ignore'), item['Rtime'].encode('utf-8', 'ignore'), item['Rcontent'].encode('utf-8', 'ignore'), item['Rliked'].encode('utf-8', 'ignore'))
                    self.db.Insert_MySQL(sql)
                except Exception as e:
                    print '插入HTINSEIDE错误' + str(e)
        if isinstance(item, DoubanJPItem):
            try:
                sql = """insert into DoubanJP (JP_id, title, author, JPtime, JPstar, href, Content, JPliked, JPdisliked, reply) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")"""%(item['JP_id'].encode('utf-8', 'ignore'), item['title'].encode('utf-8', 'ignore'), item['author'].encode('utf-8', 'ignore'), item['JPtime'].encode('utf-8', 'ignore'), item['JPstar'].encode('utf-8', 'ignore'), item['href'].encode('utf-8', 'ignore'), item['Content'].encode('utf-8', 'ignore'), item['JPliked'].encode('utf-8', 'ignore'), item['JPdisliked'].encode('utf-8', 'ignore'), item['reply'].encode('utf-8', 'ignore'))
                self.db.Insert_MySQL(sql)
            except Exception as e:
                print '插入JP表错误' + str(e)
