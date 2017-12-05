# -*- coding: utf-8 -*-
import requests
from scrapy import Selector
from lxml import etree

a = requests.get('https://movie.douban.com/subject/27039382/comments?sort=new_score&status=P').content
selector = etree.HTML(a)
divs = selector.xpath('//div[@class="comment-item" and @data-cid]')
for div in divs:
    aa = div.xpath('div/div[@class="comment"]/h3/span[@class="comment-info"]/a/text()').extract()
    bb = div.xpath('div/div[@class="comment"]/h3/span[@class="comment-info"]/span[@class="allstar30 rating"]/@title').extract()
    cc = div.xpath('div/div[@class="comment"]/h3/span[@class="comment-info"]/span[@class="comment-time"]/text()').extract()
    dd = div.xpath('div/div[@class="comment"]/h3/span[@class="comment-vote"]/span[@class="votes"]/text()').extract()
    ee = div.xpath('div/div[@class="comment"]/p/text()').extract()
    print aa, bb, cc, dd, ee