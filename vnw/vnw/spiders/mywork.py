# -*- coding: utf-8 -*-

import scrapy
from ..items import PyjobItem
from ..pymods import xtract, parse_datetime, has_expired
from ..keywords import KWS

province = u'Nơi làm việc'
wage = u'Mức lương'
experience = u'Kinh nghiệm'
work = u'Mô tả công việc'
welfare = u'Quyền lợi được hưởng'
specialize = u'Yêu cầu công việc'
file_request = u'Yêu cầu hồ sơ'
language = u'Ngôn ngữ hồ sơ'
date_post = u'Ngày cập nhật'


class MyworkSpider(scrapy.Spider):
    name = "mywork"
    allowed_domains = ["mywork.com.vn"]
    start_urls = [("http://mywork.com.vn/tim-viec-lam/" + kw + ".html")
                  for kw in KWS]

    def parse(self, resp):
        url = resp.url
        keyword = url.split("/tim-viec-lam/")[1].split(".")[0]
        for href in resp.xpath('//div[@class="item "]/div/a/@href').extract():
            request = scrapy.Request(resp.urljoin(href), self.parse_content)
            request.meta["keyword"] = keyword
            yield request

        try:
            if resp.xpath('//div[@class="mywork-pages pagination"]/a/@class').\
                    extract()[-1] != u'disabled':
                next_page = resp.xpath('//div[@class="mywork-pages pagination"'
                                       ']/a/@href').extract()[-1]
                yield scrapy.Request(resp.urljoin(next_page), self.parse)
        except IndexError:
            print "Page none!"

    def parse_content(self, resp):
        item = PyjobItem()
        expiry_date = xtract(resp,
                             '//div[@class="job_deadline"]/text()'
                             ).split(': ')[1].strip(')')

        if has_expired(expiry_date):
            yield {}
        item["keyword"] = resp.meta["keyword"]
        item["url"] = resp.url
        item["name"] = xtract(resp, '//div[@class="title-job-info"]/text()'
                                    '')
        item["company"] = xtract(resp,
                                 '//h1[@class="fullname-company"]/text()')
        item["address"] = xtract(resp, '//p[@class="address-company mw-ti"'
                                       ']/text()')
        post_date = xtract(
            resp, '//span[@class="job_update"]/text()'
        ).split(': ')[1]
        item["post_date"] = parse_datetime(post_date)
        item["expiry_date"] = parse_datetime(expiry_date)

        for desjob in resp.xpath('//div[@class="desjob-company"]'):
            kws = xtract(desjob, 'h4/text()')
            if province == kws:
                item["province"] = xtract(desjob, 'span/a/text()')
            if wage == kws:
                if xtract(desjob, 'span/text()'):
                    item["wage"] = xtract(desjob, 'span/text()')
                else:
                    item["wage"] = xtract(desjob, 'text()')
            if experience == kws:
                item["experience"] = xtract(desjob,  'p/span/text()')
            if work == kws:
                if xtract(desjob, 'p/text()') != u'':
                    item["work"] = xtract(desjob, 'p/text()')
                else:
                    item["work"] = xtract(desjob, 'div/text()')
            if welfare == kws:
                if not xtract(desjob, 'p/span/text()'):
                    item["welfare"] = xtract(desjob, 'p/span/text()')
                item["welfare"] = xtract(desjob, 'p/text()')
            if specialize == kws:
                if xtract(desjob, 'p/text()') != u' ':
                    item["specialize"] = xtract(desjob, 'p/text()')
                elif xtract(desjob, 'p/text()'):
                    item["specialize"] = xtract(desjob, 'div/text()')
            if file_request == kws:
                if len(xtract(desjob, 'p/text()')) > 10:
                    item["file_request"] = xtract(desjob, 'p/text()')
                else:
                    item["file_request"] = xtract(desjob, 'p/span/text()')
            if language == kws:
                item["language"] = xtract(desjob, 'p/text()')
        yield item
