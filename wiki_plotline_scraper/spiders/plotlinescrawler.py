from __future__ import with_statement
from scrapy.spider import BaseSpider
from scrapy.http.request import Request
from scrapy.conf import settings
from plotlineparser import PlotlineParser

import pymongo
import json
import urllib
import unicodedata

class PlotlinesCrawler(BaseSpider):

    name = 'plotlines'
    allowed_domains = ['google.com', 'wikipedia.org']

    def __init__(self):
        conn = pymongo.Connection(settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.start_urls = self.gen_start_urls()

    def gen_start_urls(self):

        def is_ascii(s):
            return all(ord(c) < 128 for c in s)

        def clean_parsed_string(string):
            if len(string) > 0:
                ascii_string = string
                if is_ascii(ascii_string) == False:
                    ascii_string = unicodedata.normalize('NFKD', ascii_string).encode('ascii', 'ignore')
                return str(ascii_string)
            else:
                return None

        with open(settings['MOVIES_FILE'], 'rb') as fin:
            data = json.load(fin)
        start_urls = []
        for movie_file in data:
            qtext = '%s + %s + film + wikipedia' % (clean_parsed_string(movie_file['film']) , str(movie_file['year']))
            query = urllib.urlencode({'q': qtext})
            start_urls.append('http://www.google.com/search?%s&btnI' % query)
        return start_urls

    def parse(self, response):
        parser = PlotlineParser(response)
        return parser.parse() 

        
