# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanDPItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Uname = scrapy.Field() #短评用户
    Star = scrapy.Field() #短评星级
    DPtime = scrapy.Field() #短评时间
    Liked = scrapy.Field() #短评点赞
    Content = scrapy.Field() #短评内容

class DoubanHTItem(scrapy.Item): #帖子内容和回复分两个表，用HT_id关联
    HT_id = scrapy.Field() #话题id
    title = scrapy.Field() #话题标题
    author = scrapy.Field() #话题作者
    reply = scrapy.Field() #话题回复
    HT_href = scrapy.Field() #话题地址
    HTtime = scrapy.Field() #话题发布时间
    sign = scrapy.Field() #用于做pipeline的分割，避免item重复
    HT_Content = scrapy.Field() #话题内容
    Rname = scrapy.Field() #回复用户
    Rtime = scrapy.Field() #回复时间
    Rcontent = scrapy.Field() #回复内容
    Rliked = scrapy.Field() #回复点赞数

class DoubanJPItem(scrapy.Item):
    JP_id = scrapy.Field() #剧评id
    title = scrapy.Field() #剧评标题
    author = scrapy.Field() #剧评作者
    JPtime = scrapy.Field() #剧评时间
    JPstar = scrapy.Field() #剧评打星
    href = scrapy.Field() #主题链接
    Content = scrapy.Field() #剧评文本内容
    JPliked = scrapy.Field() #剧评点赞
    JPdisliked = scrapy.Field() #剧评踩
    reply = scrapy.Field() #剧评回复数
    Rname = scrapy.Field()  # 回复用户
    Rtime = scrapy.Field()  # 回复时间
    Rcontent = scrapy.Field()  # 回复内容



