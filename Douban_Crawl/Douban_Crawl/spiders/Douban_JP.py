# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from Douban_Crawl.With_DB import Redis_DB
from Douban_Crawl.items import DoubanJPItem
from scrapy import Request
from scrapy import Selector

class Douban_JP(RedisSpider):
    name = 'JPSpider'
    redis_key = 'JP_urls'

    def parse(self, response):
        selector = Selector(response)
        divs = selector.xpath('//div[@class="article"]/div[@class="review-list  "]/div[@data-cid]')
        for div in divs:
            try:
                author = div.xpath('div[@id]/header[@class="main-hd"]/a[@class="name"]/text()').extract()[0]
            except:
                author = ''
            try:
                JPstar = div.xpath('div[@id]/header[@class="main-hd"]/span[@property="v:rating"]/@title').extract()[0]
            except:
                JPstar = ''
            try:
                JPtime = div.xpath('div[@id]/header[@class="main-hd"]/span[@class="main-meta"]/text()').extract()[0]
            except:
                JPtime = ''
            try:
                title = div.xpath('div[@id]/div[@class="main-bd"]/h2/a/text()').extract()[0]
            except:
                title = ''
            try:
                href = div.xpath('div[@id]/div[@class="main-bd"]/h2/a/@href').extract()[0]
            except:
                href = ''
            try:
                JPliked = div.xpath('div[@id]/div[@class="main-bd"]/div[@class="action"]/a[@class="action-btn up"]/span[@id]/text()').extract()[0]
            except:
                JPliked = ''
            try:
                JPdisliked = div.xpath('div[@id]/div[@class="main-bd"]/div[@class="action"]/a[@class="action-btn down"]/span[@id]/text()').extract()[0]
            except:
                JPdisliked = ''
            try:
                reply = div.xpath('div[@id]/div[@class="main-bd"]/div[@class="action"]/a[@class="reply"]/text()').extract()[0]
            except:
                reply = ''
            try:
                JP_id = div.xpath('div[@id]/@id').extract()[0]
            except:
                JP_id = ''
            yield Request(url=href, callback=self.parse_content, meta={'author':author, 'JPstar':JPstar, 'JPtime':JPtime, 'title':title, 'href':href, 'JPliked':JPliked, 'JPdisliked':JPdisliked, 'reply':reply, 'JP_id':JP_id})
        try:
            next_part = selector.xpath('//div[@class="article"]/div[@class="paginator"]/span[@class="next"]/a/@href').extract()[0]
            next_url = 'https://movie.douban.com/subject/27039382/reviews' + str(next_part)
            r0 = Redis_DB(0)
            r0.Insert_Redis('JP_urls', next_url)
        except Exception as e:
            print '剧评翻页错误' + str(e)

    def parse_content(self, response):
        selector = Selector(response)
        try:
            p = selector.xpath('//div[@id="link-report"]/div[@class="review-content clearfix"]/p')
            content = ''
            for i in p:
                content += i.xpath('text()').extract()[0]
        except Exception as e:
            print '组合content错误' + str(e)
        try:
            item = DoubanJPItem()
            item['JP_id'] = str(response.meta['JP_id'])
            item['title'] = response.meta['title']
            item['author'] = response.meta['author']
            item['JPtime'] = response.meta['JPtime']
            item['JPstar'] = response.meta['JPstar']
            item['href'] = response.meta['href']
            item['Content'] = content
            item['JPliked'] = str(response.meta['JPliked'])
            item['JPdisliked'] = str(response.meta['JPdisliked'])
            item['reply'] = str(response.meta['reply'])
            yield item
        except Exception as e:
            print 'item赋值错误' + str(e)

