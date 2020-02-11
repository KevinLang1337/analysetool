import scrapy

class QuotesSpider(scrapy.Spider):
    name = "jokes"
    start_urls = ["http://quotes.toscrape.com"]

    def parse(self, response):
    
        quotes = response.xpath("//div[@class='quote']")
        
        #css('div.quote')
        for quote in quotes:
            yield {

                'text': quote.xpath(".//*[@class='text']/text()").get(),
                # 'text': quote.css('.text::text').get(),
                'author': quote.xpath(".//*[@class='author']/text()").get(),
                'tags': quote.xpath(".//*[@class='tag']/text()").getall(),
            
                # 'author': quote.css('.author::text').get(),
                # 'tags': quote.css('.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        
   
