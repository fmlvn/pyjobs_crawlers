# -*- coding: utf-8 -*-

import scrapy
from ..items import PyjobItem
from ..pymods import xtract

KWS = ["python", "django", "flask", "openstack", "pyramid", "pylons", "web2py"]


class VnwSpider(scrapy.Spider):
    name = "vietnamwork"
    allowed_domains = ["vietnamwork.com"]
    start_urls = [
        ("http://www.vietnamworks.com/" + kw + "-kv") for kw in KWS
    ]

    def parse(self, resp):
        if resp.xpath('//a[@class="job-title text-clip text-lg"]') != []:
            urls = resp.xpath(
                '//a[@class="job-title text-clip text-lg"]/@href').extract()
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_content)


    def parse_content(self, resp):
        item = PyjobItem()
        item["name"] = xtract(resp, '//h1/text()')
        item["company"] = xtract(resp,
            '//span[@class="company-name text-lg block"]/strong/text()')
        item["address"] = xtract(resp,
            '//span[@class="company-address block"]/text()')
        item["province"] = xtract(resp, '//span[@itemprop="address"]/a/text()')
        item["wage"] = xtract(resp, '//div[@class="col-sm-12"]/div/text()')
        item["skill"] = xtract(resp, '//span[@class="tag-name"]/text()')
        item["work"] = xtract(resp, '//div[@id="job-description"]/text()')
        item["specialize"] = xtract(resp, '//div[@class=""]/text()')
        item["information"] = xtract(resp,
                                     '//span[@id="companyprofile"]/text()')
        item["contact"] = resp.xpath('//div[@class="company-info"]/p/strong/'
                                     'text()').extract()[0].strip()
        item["size"] = resp.xpath('//div[@class="company-info"]/p/strong/'
                                  'text()').extract()[1].strip()
        item["logo"] = xtract(resp, '//img[@class="logo img-responsive"]/@src')
        yield item
