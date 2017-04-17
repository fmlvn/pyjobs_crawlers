import logging
import requests
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)
REQUIRED_FIELDS = ['name', 'province', 'url', 'work', 'specialize']


def xtract_item(item):
    for key, value in item.iteritems():
        for num in range(4):
            # use 4 loops to handle all cases because there are 4 characters
            value = value.strip('-').strip().strip('+').strip(':')
        item[key] = value
    return item


class VnwPipeline(object):
    def process_item(self, item, spider):
        return item


class ValidatePipeline(object):
    def process_item(self, item, spider):
        if not item:
            logger.error('Drop job, item is empty')
            raise DropItem
        try:
            kv = {kw: item[kw] for kw in REQUIRED_FIELDS}
        except KeyError as e:
            logger.error('Drop job: %s %s, missing required key %r',
                         item.get('name', 'MISSING'),
                         item.get('url', 'MISSING'),
                         e)
            raise DropItem
        for k, v in kv.iteritems():
            if v.strip() == '':
                logger.error('Drop job: %s %s, required key %r is empty',
                             item.get('name', 'MISSING'),
                             item.get('url', 'MISSING'),
                             k)
                raise DropItem

        item = xtract_item(item)
        return item


class APIPipeline(object):
    collection_name = 'scrapy_items'

    def __init__(self):
        self.url = 'http://127.0.0.1:5000/python'

    def process_item(self, item, spider):
        try:
            requests.post(self.url, json=item._values)
        except KeyError as e:
            logger.error('Error when posting: %s', e)
