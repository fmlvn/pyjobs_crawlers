import logging
import requests

logger = logging.getLogger(__name__)
KWS = ['name', 'post_date', 'company', 'province', 'url']


class ElasticSearchPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, address, index, type, port=9200):
        self.url = 'http://{0}:{1}/{2}/{3}'.format(address, port, index, type)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            address=crawler.settings.get('ES_ADDRESS'),
            port=crawler.settings.get('ES_PORT', 9200),
            index=crawler.settings.get('ES_INDEX'),
            type=crawler.settings.get('ES_TYPE')
        )

    def process_item(self, item, spider):
        try:
            requests.post(self.url, json=item._values)
        except Exception as e:
            logger.error('Cannot POST job %s, error: %s',
                         item['name'],
                         e,
                         exc_info=True)


class VnwPipeline(object):
    def process_item(self, item, spider):
        return item


class APIPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self):
        self.url = 'http://127.0.0.1:5000/python'

    def process_item(self, item, spider):
        for kw in KWS:
            try:
                if item[kw].strip():
                    continue
                else:
                    logger.error('Empty value: %s',  kw)
            except KeyError as e:
                logger.error('Not found %s, error: %s', kw, e)
        requests.post(self.url, json=item._values)
