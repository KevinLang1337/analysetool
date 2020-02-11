import scrapy

class webcrawler(scrapy.Spider):
    name = "quotes"

    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        print("erste Spider")
        pass