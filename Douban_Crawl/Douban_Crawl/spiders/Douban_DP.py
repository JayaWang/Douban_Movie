# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from Douban_Crawl.With_DB import Redis_DB
from Douban_Crawl.items import DoubanDPItem
import time
from scrapy.selector import Selector

class Douban_DP(RedisSpider):
    name = 'DPSpider'
    redis_key = 'DP_urls'

    def parse(self, response):
        selector = Selector(response)
        divs = selector.xpath('//div[@class="comment-item" and @data-cid]')
        for div in divs:
            try:
                item = DoubanDPItem()
                try:
                    item['Uname'] = div.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/a/text()').extract()[0]
                except:
                    item['Uname'] = ''
                try:
                    item['Star'] = div.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span/@title').extract()[0]
                except:
                    item['Star'] = ''
                try:
                    item['DPtime'] = div.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span[@class="comment-time "]/@title').extract()[0]
                except:
                    item['DPtime'] = ''
                try:
                    item['Liked'] = str(div.xpath('div[@class="comment"]/h3/span[@class="comment-vote"]/span[@class="votes"]/text()').extract()[0])
                except:
                    item['Liked'] = ''
                try:
                    item['Content'] = div.xpath('div[@class="comment"]/p/text()').extract()[0]
                except:
                    item['Content'] = ''
                yield item
            except Exception as e:
                print ('提取短评错误' + str(e))
        try:
            next_part = selector.xpath('//div[@class="article"]/div[@id="comments"]/div[@id="paginator"]/a[@class="next"]/@href').extract()[0]
            next_url = 'https://movie.douban.com/subject/27039382/comments' + str(next_part)
            r0 = Redis_DB(0)
            r0.Insert_Redis('DP_urls', next_url)
        except Exception as e:
            print ('翻页错误/翻到底了' + str(e))




