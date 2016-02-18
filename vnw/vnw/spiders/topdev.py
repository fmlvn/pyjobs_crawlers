# -*- coding: utf-8 -*-

import scrapy
from ..keywords import KWS
from ..items import PyjobItem
from ..pymods import xtract, parse_datetime
import time

class TopdevSpider(scrapy.Spider):
    name = "topdev"
    allowed_domains = ["topdev.vn"]
    start_urls = [
        ("https://topdev.vn/search/keywords/" + kw) for kw in KWS
    ]

    def parse(self, resp):
        if not resp.xpath('//div[@class="col-lg-12 col-md-12 col-sm-1'
                          '2 col-xs-12 no-padding title-jobs"]/@href')\
                    .extract():
            for href in resp.xpath('//div[@class="col-lg-12 col-md-12 col-sm-1'
                                   '2 col-xs-12 no-padding title-jobs"]/a/'
                                   '@href').extract():
                yield scrapy.Request(href, self.parse_content)

    def parse_content(self, resp):
        item = PyjobItem()
        item["name"] = xtract(resp, '//div[@class="col-lg-12 col-md-12 col-sm-'
                                    '12 col-xs-12 title_name_job no-padding"]/'
                                    'h1/text()')
        item["province"] = resp.xpath('//div[@class="col-md-12 col-lg-12 col'
                                      '-xs-12 col-sm-12 no-padding"]/span/'
                                      'text()').extract()[0]
        for span in resp.xpath('//div[@class="intro-jobs col-lg-12 col-md-12 '
                               'col-sm-12 col-xs-12 no-padding margin-top-5'
                               ' margin-bottom-5"]'):
            wage = xtract(span, 'span[1]/text()')
            item["wage"] = wage.split(':')[1].strip()
            experience = xtract(span, 'span[2]/text()')
            item["experience"] = experience.split(': ')[1]
            expiry = xtract(span, 'span[4]/text()')
            expiry = expiry.split(' :')[1]
            item["expiry_date"] = parse_datetime(expiry)
        for li in resp.xpath('//div[@id="desc_job"]'):
            list_text = []
            p = xtract(li, 'p/text()')
            list_text.append(p)
            pstrong = xtract(li, 'p/strong/text()')
            list_text.append(pstrong)
            ullip = xtract(li, 'ul/li/p/text()')
            list_text.append(ullip)
            pp = xtract(li, 'p/p/text()')
            list_text.append(pp)
            pbr = xtract(li, 'p/br/text()')
            list_text.append(pbr)
            pspan = xtract(li, 'p/span/text()')
            list_text.append(pspan)
            pemstrong = xtract(li, 'p/em/strong/text()')
            list_text.append(pemstrong)
            pstrongem = xtract(li, 'p/strong/em/text()')
            list_text.append(pstrongem)
            pstrongspan = xtract(li, 'p/strong/span/text()')
            list_text.append(pstrongspan)
            pspanem = xtract(li, 'p/span/em/text()')
            list_text.append(pspanem)
            ulli = xtract(li, 'ul/li/text()')
            list_text.append(ulli)

        item["content"] = '|'.join(list_text).strip()
        yield item