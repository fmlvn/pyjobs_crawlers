# -*- coding: utf-8 -*-

import scrapy
from ..keywords import KWS
from ..items import PyjobItem


class TopdevSpider(scrapy.Spider):
    name = "topdev"
    allowed_domains = ["topdev.vn"]
    start_urls = [
        ("https://topdev.vn/search?q=" + kw) for kw in KWS
    ]

    def parse(self, resp):
        if not resp.xpath('div[@class="job-item-info relative"]'
                          '/h3/@href').extract():
            for href in resp.xpath('//div[@class="job-item-info relative"]'
                                   '/h3/a/@href').extract():
                yield scrapy.Request(href, self.parse_content)

    def parse_content(self, resp):
        item = PyjobItem()
        item["url"] = resp.url
        item["name"] = resp.xpath('//div[@class="job-header-info"]'
                                  '/h1/text()').extract_first()
        item["province"] = resp.xpath('//p[@class="work-location"]'
                                      '/span/a/text()').extract_first()
        item["wage"] = resp.xpath('//div[contains(@class, "salary")]'
                                  '/span/text()').extract_first()
        item["post_date"] = resp.xpath('//div[@id="image-employer"]'
                                       '/*/*/div[2]/div[@class="'
                                       'pull-right text-gray-light"]'
                                       '/div[2]/text()').extract_first()
        item["company"] = resp.xpath('//div[@class="job-header-info"]'
                                     '/span[contains(@class, '
                                     '"company-name")]/strong/'
                                     'text()').extract_first()
        if not resp.xpath('//div[@id="job-requirement"]'
                          '/*/*/ul/li/text()').extract():
            item["content"] = resp.xpath('//div[@id="job-requirement"]'
                                         '/*/*/*/ul/li/text()').extract()
        else:
            item["content"] = resp.xpath('//div[@id="job-requirement"]'
                                         '/*/*/ul/li/text()').extract()

        item["specialize"] = ''
        item["work"] = ''
        item["experience"] = ''
        item["expiry_date"] = ''

        yield item
