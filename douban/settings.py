# -*- coding: utf-8 -*-

# Scrapy settings for douban project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'douban (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Cookie': 'bid=sRvyFl0jTQw; douban-fav-remind=1; ll="118267"; gr_user_id=4205e607-97e8-4dfe-9975-3cb8940565b5; _vwo_uuid_v2=DBAEF464BB1861A75F870887FBBADC529|77c76a07db0134b79eb46f78056ed205; __gads=ID=10a86b515179eec8:T=1559907381:S=ALNI_MZt9ECoDrxE4lmv7DMbizgGBqPxtg; __yadk_uid=AwmfiSfKAtNvwLNyVRFi2geDZEoQMEOQ; viewed="1406522_3272929_33425120_3179585_33409015_26981519_25779298_30293801_30175598_26829016"; __utmc=30149280; __utmz=30149280.1565923530.16.12.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; dbcl2="202065201:65vJxjQco1w"; ck=a_DK; push_noty_num=0; push_doumail_num=0; __utmv=30149280.20206; __utmc=81379588; ct=y; ap_v=0,6.0; __utma=30149280.733410425.1557716653.1565923530.1565935312.17; __utmt=1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=c31e5c1c-138f-4eb6-960f-e0912a14c271; gr_cs1_c31e5c1c-138f-4eb6-960f-e0912a14c271=user_id%3A1; __utmt_douban=1; __utma=81379588.460248323.1557716663.1565923802.1565935439.4; __utmz=81379588.1565935439.4.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1565935439%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_c31e5c1c-138f-4eb6-960f-e0912a14c271=true; _pk_id.100001.3ac3=51a50168a205a612.1557716663.4.1565935453.1565926369.; __utmb=30149280.5.10.1565935312; __utmb=81379588.3.10.1565935439',
    'Host': 'book.douban.com',
    'Referer': 'https://book.douban.com/tag/?icn=index-nav',
}


# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'douban.middlewares.DoubanSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'douban.middlewares.DoubanDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'douban.pipelines.DoubanPipeline': 300,
    'douban.pipelines.MongoPipeline': 400,
}

MONGO_URI = 'localhost' # 主机名
MONGO_DB = 'Douban' # 库名

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
