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
    name = 'mywork'
    allowed_domains = ['mywork.com.vn']
    start_urls = [('https://mywork.com.vn/tim-viec-lam/' + kw + '.html')
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
                next_page = resp.xpath('//div[contains(@class, '
                                       '"mywork-pages pagination")]/'
                                       '/a/@href').extract()[-1]
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
        item["name"] = xtract(resp, '//div[@class="title-job-info"]/h1/text()'
                                    '')
        item["company"] = xtract(resp,
                                 '//h1[@class="comp-name"]/a/text()')
        item["province"] = xtract(
            resp,
            '//div[@class="job-company-info"]/p/b/span/a/text()'
        )
        post_date = xtract(
            resp, '//div[@class="job-current-info"]/div[2]/text()'
        ).split(': ')[1]
        item["post_date"] = parse_datetime(post_date)
        item["expiry_date"] = parse_datetime(expiry_date)
        item["address"] = xtract(
            resp,
            '//p[@class="address-company mw-ti-new"]/text()'
        )

        if not resp.xpath('//div[@class="job-company-info"]/p[last()]'
                          '/b/span/text()').extract():
            item["wage"] = ' - '.join(
                resp.xpath('//div[@class="job-company-info"]/p[last()]'
                           '/b/text()').extract())
        else:
            item["wage"] = ' - '.join(
                resp.xpath('//div[@class="job-company-info"]/p[last()]'
                           '/b/span/text()').extract())

        desjob = resp.xpath('//div[@class="desjob-company"]')[1].extract()
        item["specialize"] = desjob.splitlines()[2].strip(
            ).strip('-').strip().replace('<br>', '|').replace('-', '')
        yield item
