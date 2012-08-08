# Scrapy settings for wiki_plotline_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'wiki_plotline_scraper'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['wiki_plotline_scraper.spiders']
NEWSPIDER_MODULE = 'wiki_plotline_scraper.spiders'
DEFAULT_ITEM_CLASS = 'wiki_plotline_scraper.items.WikiPlotlineScraperItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = ['wiki_plotline_scraper.pipelines.WikiPlotlineScraperPipeline',]

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'wiki_plotlines'
MONGODB_COLLECTION = 'master'

# Input file as [['film':'film-name', 'year':film-year],...] json file
MOVIES_FILE = '/home/bharani/code/movies.json'
