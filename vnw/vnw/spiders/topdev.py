# -*- coding: utf-8 -*-

import scrapy
from ..keywords import KWS
from ..items import PyjobItem
from ..pymods import xtract


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
        item["name"] = xtract(resp, '//div[@class="job-header-info"]'
                                    '/h1/text()')
        if xtract(resp, '//p[@class="work-location"]'
                        '/span/a/text()'):
            item["province"] = xtract(resp, '//p[@class="work-location"]'
                                            '/span/a/text()')
        else:
            item["province"] = 'Viet Nam'
        item["wage"] = xtract(resp, '//div[contains(@class, "salary")]'
                                    '/span/text()')
        item["post_date"] = xtract(resp, '//div[@id="image-employer"]'
                                         '/*/*/div[2]/div[@class="'
                                         'pull-right text-gray-light"]'
                                         '/div[2]/text()')
        item["company"] = xtract(resp, '//div[@class="job-header-info"]'
                                       '/span[contains(@class, '
                                       '"company-name")]/strong/'
                                       'text()')
        if xtract(resp, '//div[@id="job-description"]/ul/li'):
            item["work"] = xtract(resp, '//div[@id="job-description"]'
                                        '/ul/li/text()')
        elif xtract(resp, '//div[@id="job-description"]/div'):
            item["work"] = xtract(resp, '//div[@id="job-description"]'
                                        '/div/text()')
        else:
            item["work"] = xtract(resp, '//div[@id="job-description"]'
                                        '/p/text()')

        if xtract(resp, '//div[@id="job-requirement"]'
                        '/*/*/ul/li/text()'):
            item["specialize"] = xtract(resp, '//div[@id="job-requirement"]'
                                              '/*/*/ul/li/text()')
        else:
            item["specialize"] = xtract(resp, '//div[@id="job-requirement"]'
                                              '/*/*/*/ul/li/text()')

        yield item
