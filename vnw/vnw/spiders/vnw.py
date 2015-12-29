__author__ = 'daivq'

import scrapy

KWS = ["python", "django", "flask", "openstack", "pyramid", "pylons", "web2py"]


def xtract(response, xpath):
    li = []
    xtracts = response.xpath(xpath).extract()
    for xts in xtracts:
        xts = xts.strip()
        li.append(xts)
    return u'|'.join(li)


class VnwItem(scrapy.Item):
    name = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    province = scrapy.Field()
    wage = scrapy.Field()
    welfare = scrapy.Field()
    skill = scrapy.Field()
    work = scrapy.Field()
    specialize = scrapy.Field()
    information = scrapy.Field()
    contact = scrapy.Field()
    size = scrapy.Field()
    logo = scrapy.Field()

class VnwSpider(scrapy.Spider):
    name = "vietnamwork"
    allow_domains = ["vietnamwork.com"]
    start_urls = [
        ("http://www.vietnamworks.com/" + kw + "-kv") for kw in KWS
    ]

    def parse(self, response):
        if response.xpath('//a[@class="job-title text-clip text-lg"]') != []:
            urls = response.xpath(
                '//a[@class="job-title text-clip text-lg"]/@href').extract()
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_content)


    def parse_content(self, resp):
        item = VnwItem()
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