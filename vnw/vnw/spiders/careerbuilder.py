#! -*- coding: utf-8 -*-

import scrapy
from ..items import PyjobItem
from ..keywords import KWS
from ..pymods import xtract, parse_datetime


experience = u'Kinh nghiệm: '
level = u'Cấp bậc: '
wage = u'Lương: '
expiry_date = u'Hết hạn nộp: '
contact = u'Người liên hệ: '


class CareerbuilderSpider(scrapy.Spider):
    name = 'careerbuilder'
    allowed_domains = ["careerbuilder.vn"]
    start_urls = [
        ('http://careerbuilder.vn/viec-lam/' + KW +
         '-k-vi.html') for KW in KWS
    ]

    def parse(self, resp):
        url = resp.url
        keyword = url.split("/viec-lam/")[1].split("-k-")[0]
        for href in resp.xpath('//h3[@class="job"]/a/@href').extract():
            request = scrapy.Request(href, self.parse_content)
            request.meta["keyword"] = keyword
            yield request

        if resp.xpath('//a[@class="right"]'):
            next_page = resp.xpath('//a[@class="right"]/@href').extract()[0]
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_content(self, resp):
        item = PyjobItem()
        item["keyword"] = resp.meta["keyword"]
        item["url"] = resp.url
        item["name"] = xtract(resp, '//h1[@itemprop="title"]/text()')
        item["company"] = xtract(resp, '//div[@class="tit_company"]/text()')
        item["address"] = xtract(resp,
                                 '//label[@itemprop="addressLocality"]/text()')
        if xtract(resp, '//p[@itemprop="jobLocation"]'):
            item["province"] = xtract(resp,
                                      '//p[@itemprop="jobLocation"]/a/text()')
        else:
            item["province"] = xtract(resp,
                                      '//b[@itemprop="jobLocation"]/a/text()')

        if xtract(resp, '//div[@itemprop="description"]/ul/li/text()'):
            item["work"] = xtract(
                    resp,
                    '//div[@itemprop="description"]/ul/li/text()'
            )
        else:
            item["work"] = xtract(resp,
                                  '//div[@itemprop="description"]/p/text()')

        if xtract(resp, '//div[@itemprop="experienceRequirements"]/ul/li'):
            item["specialize"] = xtract(
                    resp,
                    '//div[@itemprop="experienceRequirements"]'
                    '/p/strong/text()'
            ) + u'|' + xtract(
                    resp,
                    '//div[@itemprop="experienceRequirements"]'
                    '/ul/li/text()'
            )
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

            if kw == expiry_date:
                expiry = xtract(kws, 'text()')
                if u'/' not in expiry:
                    item["expiry_date"] = parse_datetime(expiry)
                else:
                    expiry = expiry.split('/')
                    expiry = '-'.join(expiry)
                    item["expiry_date"] = parse_datetime(expiry)

        for lbs in resp.xpath('//p[@class="TitleDetailNew"]/label'):
            lb = xtract(lbs, 'text()')
            if lb == contact:
                item["contact"] = xtract(lbs, 'strong/text()')

        try:
            post_date = xtract(resp, '//div[@class="datepost"]/text()')
            post_date = post_date.split(': ')[1].split('/')
            post_date = '-'.join(post_date)
            item["post_date"] = parse_datetime(post_date)
        except IndexError:
            item["post_date"] = ''
        item["website"] = xtract(resp, '//span[@class="MarginRight30"]/text()')

        yield item
