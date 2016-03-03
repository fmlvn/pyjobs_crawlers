# -*- coding: utf-8 -*-

import scrapy
from ..items import PyjobItem
from ..pymods import xtract
from ..keywords import KWS
from ..pymods import parse_datetime
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.conf import settings


class VnwSpider(InitSpider):
    name = "vietnamwork"
    allowed_domains = ["vietnamwork.com"]
    login_page = "http://www.vietnamworks.com/login"
    start_urls = [
        ("http://www.vietnamworks.com/" + kw + "-kw") for kw in KWS
    ]

    
    def init_request(self):
        return Request(url=self.login_page, callback=self.login)


    def login(self, resp):
        user = settings.get('VIETNAMWORK_USERNAME')
        password = settings.get('VIETNAMWORK_PASSWORD')
        return FormRequest.from_response(resp,
            method='POST',
            formdata={'form[username]': user, 'form[password]': password },
            callback=self.check_login,
            dont_filter=True
            )


    def check_login(self, resp):
        return self.initialized()

    def parse(self, resp):
        url = resp.url
        keyword = url.split('.com/')[1].split('-kw')[0]
        for div in resp.xpath('//div[@class="col-sm-9 col-sm-pull-3"]'):
            post_date = div.xpath('div/div/div/span/span/span/text()').extract()[0]
            post_date = post_date.split(': ')[1]
            post_date = '-'.join(post_date.split('/'))
            convert_post_date = parse_datetime(post_date)
            for url in div.xpath('div/a/@href').extract():
                request = scrapy.Request(url, self.parse_content, dont_filter=True)
                request.meta["keyword"] = keyword
                request.meta["post_date"] = convert_post_date
                yield request

    def parse_content(self, resp):
        item = PyjobItem()
        item["url"] = resp.url
        item["keyword"] = resp.meta["keyword"]
        item["post_date"] = resp.meta["post_date"]
        item["name"] = xtract(resp, '//h1/text()')
        item["company"] = xtract(resp,
                                 '//span[@class="company-name text-lg block"]'
                                 '/strong/text()')
        item["address"] = xtract(resp, '//span[@class="company-address block"]'
                                       '/text()')
        item["province"] = xtract(resp, '//span[@itemprop="address"]/a/text()')
        item["wage"] = xtract(resp, '//span[@class="orange bold-700 text-lg"]/text()')
        item["work"] = xtract(resp, '//div[@id="job-description"]/text()')
        item["specialize"] = xtract(resp, '//div[@class=""]/text()')
        item["information"] = xtract(resp,
                                     '//span[@id="companyprofile"]/text()')
        item["contact"] = resp.xpath('//div[@class="company-info"]/p/strong/'
                                     'text()').extract()[0].strip()
        try:
            item["size"] = resp.xpath('//div[@class="company-info"]/p/strong/'
                                      'text()').extract()[1].strip()
        except IndexError:
            item["size"] = ''
        item["logo"] = xtract(resp, '//img[@class="logo img-responsive"]/@src')
	item["expiry_date"] = ''

        yield item
        
