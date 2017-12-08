# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from Douban_Crawl.With_DB import Redis_DB
from Douban_Crawl.items import DoubanHTItem
from scrapy.selector import Selector
from scrapy import Request

class Douban_HT(RedisSpider):
    name = 'HTSpider'
    redis_key = 'HT_urls'

    def parse(self, response):
        selector = Selector(response)
        divs = selector.xpath('//div[@class="discussion-posts"]/table[@id="posts-table"]/tr[@class and @data-id]')
        for div in divs:
            try:
                try:
                    HT_id = div.xpath('@data-id').extract()[0]
                except:
                    HT_id = ''
                try:
                    title = div.xpath('td[1]/a/text()').extract()[0]
                except:
                    title = ''
                try:
                    author = div.xpath('td[2]/a/text()').extract()[0]
                except:
                    author = ''
                try:
                    HT_href = div.xpath('td[1]/a/@href').extract()[0]
                except:
                    HT_href = ''
                try:
                    reply = div.xpath('td[3]/text()').extract()[0]
                except:
                    reply = ''
                yield Request(url=HT_href, callback=self.parse_content, meta={'HT_id': HT_id, 'title': title, 'author': author, 'HT_href': HT_href, 'reply': reply})
            except Exception as e:
                print '获取主题主页错误' + str(e)
        try:
            next_part = selector.xpath('//div[@class="article"]/div[@class="paginator"]/span[@class="next"]/a/@href').extract()[0]
            next_url = 'https://movie.douban.com/subject/27039382/discussion/' + str(next_part)
            r0 = Redis_DB(0)
            r0.Insert_Redis('HT_urls', next_url)
        except Exception as e:
            print 'HT翻页错误' + str(e)

    def parse_content(self, response):
        selector = Selector(response)
        try:
            item = DoubanHTItem()
            item['sign'] = 'OUT'
            item['HT_id'] = str(response.meta['HT_id'])
            item['title'] = response.meta['title']
            item['author'] = response.meta['author']
            item['HT_href'] = response.meta['HT_href']
            item['reply'] = str(response.meta['reply'])
            try:
                item['HTtime'] = selector.xpath('//div[@class="post-author"]/div[@class="post-author-info"]/span[@class="post-publish-date"]/text()').extract()[0]
                p = selector.xpath('//div[@class="post-content"]/div[@id="link-report"]/span/p')
                content = ''
                for i in p:
                    content += i.xpath('text()').extract()[0]
                item['Content'] = content
            except Exception as e:
                print 'content拼接有问题,给个空' + str(e)
                item['Content'] = ''
            yield item
        except Exception as e:
            print '读取OUT错误' + str(e)
        divs = selector.xpath('//td[@class="post"]/div[4]/div[@class="comment-item" and @id]')
        for div in divs:
            try:
                item = DoubanHTItem()
                item['sign'] = 'INSIDE'
                item['HT_id'] = response.meta['HT_id']
                try:
                    item['Rname'] = div.xpath('div[@class="content report-comment"]/div[@class="author"]/a/text()').extract()[0]
                except:
                    item['Rname'] = ''
                try:
                    item['Rtime'] = div.xpath('div[@class="content report-comment"]/div[@class="author"]/span/text()').extract()[0]
                except:
                    item['Rtime'] = ''
                try:
                    item['Rcontent'] = div.xpath('div[@class="content report-comment"]/p/text()').extract()[0]
                except:
                    item['Rcontent'] = ''
                try:
                    item['Rliked'] = str(div.xpath('div[@class="content report-comment"]/div[@class="op-lnks"]/a[@class="comment-vote js-vote"]/text()').extract()[0])
                except:
                    item['Rliked'] = ''
                yield item
            except Exception as e:
                print '读取INSEIDE错误' + str(e)
