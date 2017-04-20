# -*- coding: utf-8 -*-

import scrapy
from ..keywords import KWS
from ..pymods import xtract
from ..items import PyjobItem


class StackoverflowSpider(scrapy.Spider):
    name = "stackoverflow"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        ("http://stackoverflow.com/jobs?sort=i&q=" + kw) for kw in KWS
    ]

    def parse(self, resp):
        url = resp.url
        keyword = url.split("q=")[1]
        for href in resp.xpath('//h2/a[@class="job-link"]/@href').extract():
            request = scrapy.Request(resp.urljoin(href), self.parse_content)
            request.meta["keyword"] = keyword
            yield request

    def parse_content(self, resp):
        address = xtract(resp, '//li[@class="location"]/text()')
        remote = xtract(resp, '//li[@class="jobSummary remote"]/text()')
        if ('Vietnam' in address) or remote == 'Remote':
            item = PyjobItem()
            item["keyword"] = resp.meta["keyword"]
            item["url"] = resp.url
            item["province"] = 'Vietnam'
            item["name"] = xtract(resp, '//a[@class="title job-link"]/text()')
            item["company"] = xtract(resp,
                                     '//a[@class="employer up-and-out"]/@href')
            item["address"] = address
            if xtract(resp, '//div[@class="description"][1]'
                            '/div/p/text()'):
                item["work"] = xtract(resp, '//div[@class="description"][1]'
                                            '/div/p/text()')
            else:
                item["work"] = xtract(resp, '//div[@class="description"][1]'
                                            '/div/ul/li/text()')
            if xtract(resp, '//div[@class="description"][2]/ul/li/text()'):
                item["specialize"] = xtract(
                    resp, '//div[@class="description"][2]/ul/li/text()')
            else:
                item["specialize"] = xtract(
                    resp, '//div[@class="description"][2]/p/text()')
            item["welfare"] = xtract(resp,
                                     '//div[@class="description"][3]/p/text()')
            item["experience"] = xtract(resp, '//li[@class="checked"]/text()')

            yield item
