# -*- coding: utf-8 -*-

import scrapy
from ..keywords import KWS
from ..items import PyjobItem
from ..pymods import xtract


class ItviecSpider(scrapy.Spider):
    name = "itviec"
    allowed_domains = ["itviec.com"]
    start_urls = [
        ("https://itviec.com/it-jobs/" + kw) for kw in KWS
    ]

    def parse(self, resp):
        if not resp.xpath('//div[@class="job__body"]'
                          '/*/a/@href').extract():
            for href in resp.xpath('//div[@class="job__body"]'
                                   '/*/*/a/@href').extract():
                yield scrapy.Request(resp.urljoin(href), self.parse_content)

    def parse_content(self, resp):
        item = PyjobItem()
        item['url'] = resp.url
        item['name'] = resp.xpath('//h1[@class="job_title"]/'
                                  'text()').extract_first()
        item["company"] = resp.xpath('//div[@class="employer-info"]/'
                                     'h3[@class="name"]/'
                                     'text()').extract_first()
        item["address"] = resp.xpath('//div[@class="address__full-address"]/'
                                     'span/text()').extract_first(
                                     ).replace('\n, ', '').replace('\n', '')
        item["expiry_date"] = ''
        item["post_date"] = ''
        item["province"] = resp.xpath('//div[@class="address__full-address"]/'
                                      'span[@itemprop="addressLocality"]/'
                                      'text()').extract_first(
                                      ).replace('\n', '')
        item["work"] = xtract(resp, ('//div[@class="job_description"]/'
                                     'div[@class="description"]/'
                                     'ul/li/text()'))
        item["specialize"] = xtract(resp, ('//div[@class="experience"]/'
                                           'ul/li/text()'))
        item["welfare"] = xtract(resp, ('//div[@class="culture_description"]/'
                                        'ul/li/text()'))
        item["wage"] = ''
        item["size"] = resp.xpath('//p[@class="group-icon"]/'
                                  'text()').extract_first().replace('\n', '')
        yield item
