# Scrapy settings for follower project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "follower"

SPIDER_MODULES = ["follower.spiders"]
NEWSPIDER_MODULE = "follower.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = ""

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {}


DOWNLOAD_HANDLERS = {
    "http": "scrapy_curl_cffi.handlers.CurlCffiDownloadHandler",
    "https": "scrapy_curl_cffi.handlers.CurlCffiDownloadHandler",
}

DOWNLOADER_MIDDLEWARES = {
    "scrapy_curl_cffi.middlewares.CurlCffiMiddleware": 200,
    "scrapy_curl_cffi.middlewares.DefaultHeadersMiddleware": 400,
    "scrapy_curl_cffi.middlewares.UserAgentMiddleware": 500,
    "scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware": None,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "follower.pipelines.FollowerPipeline": 300,
#}

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
