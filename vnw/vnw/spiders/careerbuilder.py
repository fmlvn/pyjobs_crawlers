#! -*- coding: utf-8 -*-

import scrapy
from ..items import PyjobItem
from ..keywords import KWS
from ..pymods import xtract


experience = u'Kinh nghiệm: '
level = u'Cấp bậc: '
wage = u'Lương: '
leadtime = u'Hết hạn nộp: '
contact = u'Người liên hệ: '


class CareerbuilderSpider(scrapy.Spider):
    name = "careerbuilder"
    allowed_domains = ["careerbuilder.vn"]
    start_urls = [
        ("http://careerbuilder.vn/vi/tim-viec-lam/tu-khoa/"+ KW +
         "/limit/20/sort/score/page/1") for KW in KWS
    ]
    
    def parse(self, resp):
        for href in resp.xpath('//a[@class="job"]/@href').extract():
            yield scrapy.Request(href, self.parse_content)
        
        if resp.xpath('//a[@class="right"]'):
            next_page = resp.xpath('//a[@class="right"]/@href').extract()[0]
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_content(self, resp):
        item = PyjobItem()
        item["url"] = resp.url
        item["name"] = xtract(resp, '//h1[@itemprop="title"]/text()')
        item["company"] = xtract(resp, '//span[@itemprop="name"]/text()')
        item["address"] = xtract(resp,
                                 '//label[@itemprop="addressLocality"]/text()')
        item["province"] = xtract(resp,
                                  '//b[@itemprop="jobLocation"]/a/text()')

        if xtract(resp,'//div[@itemprop="description"]/ul/li/text()'):
            item["work"] = xtract(resp,
                              '//div[@itemprop="description"]/ul/li/text()')
        else:
            item["work"] = xtract(resp,
                                  '//div[@itemprop="description"]/p/text()')

        if xtract(resp,'//div[@itemprop="experienceRequirements"]/ul/li'):
            item["specialize"] = xtract(resp,
                                    '//div[@itemprop="experienceRequirements"]'
                                    '/p/strong/text()') + u'|' + \
                                xtract(resp,
                                    '//div[@itemprop="experienceRequirements"]'
                                    '/ul/li/text()')
        else:
            item["specialize"] = \
                xtract(resp, '//div[@itemprop="experienceRequirements"]/'
                             'p/text()')

        item["other_info"] = xtract(resp, '//div[@class="MarBot20"]/'
                                          'div[@class="content_fck"]/ul/'
                                          'li/text()')
        item["information"] = xtract(resp, '//span[@id="emp_more"]/p/text()')

        for kws in resp.xpath('//ul[@class="DetailJobNew"]/li/p'):
            kw = kws.xpath('span/text()').extract()[0]
            if kw == experience:
                item["experience"] = xtract(kws, 'text()')
            if kw == level:
                item["level"] = xtract(kws, 'label/text()')
            if kw == wage:
                if xtract(kws, 'label/text()'):
                    item["wage"] = xtract(kws, 'label/text()')
                else:
                    item["wage"] = xtract(kws, 'text()')
            if kw == leadtime:
                item["leadtime"] = xtract(kws, 'text()')

        for lbs in resp.xpath('//p[@class="TitleDetailNew"]/label'):
            lb = xtract(lbs, 'text()')
            if lb == contact:
                item["contact"] = xtract(lbs, 'strong/text()')

        item["date_post"] = xtract(resp, '//div[@class="datepost"]/text()')
        item["website"] = xtract(resp, '//span[@class="MarginRight30"]/text()')
        item["logo"] = xtract(resp, '//a[@itemprop="image"]/img/@src')

        yield item

