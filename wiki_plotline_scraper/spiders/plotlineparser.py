from wiki_plotline_scraper.items import WikiPlotlineItem
from HTMLParser import HTMLParser
from scrapy.selector import HtmlXPathSelector

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
        pitem['film'] = hxs.select('//table[contains(@class, "infobox vevent")]//th[contains(@class, "summary")]/text()').extract()
        
        outds = {'text':''}

        parser = MyHTMLParser(outds)
        data = ''
        flag = False
        for line in self.response.body.split('\n'):
            if line.find('<h2><span') != -1:
                flag = True
                continue
            if flag == True:
                if line.find('<h2>') != -1: break
                data += clean_parsed_string(line)

        parser.feed(data)

        pitem['plotline'] = outds['text']
        return pitem