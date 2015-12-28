# Scrapy settings for vnw project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'vnw'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['vnw.spiders']
NEWSPIDER_MODULE = 'vnw.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

