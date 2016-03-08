import logging
import requests

logger = logging.getLogger(__name__)
KWS = ['name', 'post_date', 'company', 'province', 'url']


def xtract_item(item):
    for key, value in item.iteritems():
        for num in range(4):
            # use 4 loops to handle all cases because there are 4 characters
            value = value.strip('-').strip().strip('+').strip(':')
        item[key] = value
    return item


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
        if all(item[kw].strip() for kw in KWS):
            item = xtract_item(item)
            try:
                requests.post(self.url, json=item._values)
            except KeyError as e:
                logger.error('Error: %s', e)
        else:
            logger.error('Bad job: %s', item['name'])
