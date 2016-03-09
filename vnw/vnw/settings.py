BOT_NAME = 'vnw'
BOT_VERSION = '1.0.5'

SPIDER_MODULES = ['vnw.spiders']
NEWSPIDER_MODULE = 'vnw.spiders'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
ITEM_PIPELINES = {
	'vnw.pipelines.APIPipeline': 1000,
}

# VIETNAMWORK_USERNAME = ''
# VIETNAMWORK_PASSWORD = ''
