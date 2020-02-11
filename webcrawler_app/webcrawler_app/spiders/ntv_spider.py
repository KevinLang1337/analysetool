import scrapy

class QuotesSpider(scrapy.Spider):
    name = "ntv"
    start_urls = ["https://www.n-tv.de/"]

    def parse(self, response):
    
        news_list = response.xpath("//div[@class='stock__group']")
        teaser_list = response.xpath("//div[@class='teaser__content']")

        for news in news_list:
            yield{
                'currency':news.xpath(".//*[@class='stock__currency']/text()").get(),
                'value':news.xpath(".//*[@class='stock__value']/text()").get(),
                'percentage':news.xpath(".//*[@class='stock__percent']/text()").get()
            }
        print("####################")
        print("--------------------")
        
        for teaser in teaser_list:
            print(teaser)
            yield{
                'info':teaser.xpath(".//*[@class='teaser__infos']/span/a/text()").get(),
                'kicker':teaser.xpath(".//*[@class='teaser__kicker']/text()").get(),
                'headline':teaser.xpath(".//*[@class='teaser__headline']/text()").get(),
                'text':teaser.xpath(".//*[@class='teaser__text']/text()").get(),
                'link':teaser.xpath(".//a/@href").get()
            }
        print("--------------------")
        print("####################")
       
        
   
