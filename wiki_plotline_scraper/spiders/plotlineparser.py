from wiki_plotline_scraper.items import WikiPlotlineItem
from HTMLParser import HTMLParser
from scrapy.selector import HtmlXPathSelector

import unicodedata

class PlotlineParser():

    def __init__(self, response):
        self.response = response

    def parse(self):

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


        class MyHTMLParser(HTMLParser):
            def __init__(self, outds):
                HTMLParser.__init__(self)
                self.outds = outds
            def handle_data(self, data):
                self.outds['text'] += data

        hxs = HtmlXPathSelector(self.response)
        pitem = WikiPlotlineItem()
        film = hxs.select('//table[contains(@class, "infobox vevent")]//th[contains(@class, "summary")]/text()').extract()
        
        if len(film) > 0:
            pitem['film'] = film[0]
        else:
            split_url = self.response.url.split('/')
            split_name = split_url[len(split_url) - 1].split('(')
            pitem['film'] = split_name[0]

        print pitem['film']

        outds = {'text':''}

        parser = MyHTMLParser(outds)
        data = ''
        flag = False
        for line in self.response.body.split('\n'):
            if (flag == False) and (line.find('class="mw-headline"') != -1):
                flag = True
                continue
            elif (flag == True) and (line.find('<h2>') == -1):
                data += line
            elif (flag == True) and (line.find('<h2>') != -1):
                break


        parser.feed(data)

        pitem['plotline'] = outds['text']
        return pitem