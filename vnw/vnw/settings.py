BOT_NAME = 'vnw'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['vnw.spiders']
NEWSPIDER_MODULE = 'vnw.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'vnw.rotate_useragent.RotateUserAgentMiddleware' :400
    }
