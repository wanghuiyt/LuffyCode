# Scrapy settings for che2 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'che2'

SPIDER_MODULES = ['che2.spiders']
NEWSPIDER_MODULE = 'che2.spiders'

LOG_LEVEL = "WARNING"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'Cookie': 'userarea=110000; listuserarea=110100; fvlid=1659995788584ksKIMMeNo86m; Hm_lvt_d381ec2f88158113b9b76f14c497ed48=1659995799; sessionid=c07d75d7-3030-40f7-b88a-7eefde6d8311; sessionip=139.227.84.9; area=310113; sessionvisit=ad86c30e-8c94-445c-ae95-5277abfc9a10; sessionvisitInfo=c07d75d7-3030-40f7-b88a-7eefde6d8311|www.che168.com|102179; che_sessionid=711DE220-665E-4CB1-B905-401F6965F66E%7C%7C2022-08-09+05%3A57%3A01.159%7C%7C0; v_no=1; visit_info_ad=711DE220-665E-4CB1-B905-401F6965F66E||EF0D13F1-C5A1-47C9-8DFB-E03624BE766B||-1||-1||1; che_ref=0%7C0%7C0%7C0%7C2022-08-09+05%3A57%3A01.159%7C2022-08-09+05%3A57%3A01.159; che_sessionvid=EF0D13F1-C5A1-47C9-8DFB-E03624BE766B; sessionuid=c07d75d7-3030-40f7-b88a-7eefde6d8311; ahpvno=4; Hm_lpvt_d381ec2f88158113b9b76f14c497ed48=1659996151; ahuuid=DE3FB9DE-4A80-4FB8-9135-00DE8DF0699F; showNum=3'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'che2.middlewares.Che2SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'che2.middlewares.Che2DownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'che2.pipelines.Che2Pipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
