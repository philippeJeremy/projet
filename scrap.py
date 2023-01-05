import os
import scrapy
import logging
from scrapy.utils.request import request_fingerprint
from scrapy.crawler import CrawlerProcess

# Récupération des hôtels
class QuotesSpider1(scrapy.Spider):
    name = "spider1"
    start_urls = ['https://www.marmiton.org/recettes/index/categorie/aperitif-dinatoire/',
                    ]
    
   
    def parse(self, response):
        print(response)

        yield {
                "target" : response.css('h1.main-title::text').get(),
                "plat": response.css("h4.recipe-card__title::text").getall()
           
                }
            
        try:
            next_page = response.css('button.fc63351294.f9c5690c58').attrib["href"]
        except KeyError:
            logging.info('No next page. Terminating crawling process.')
        else:
            yield response.follow(next_page, callback=self.after_search)
                            
filename = "liste_vin_boeuf.json"

if filename in os.listdir():
        os.remove( filename)
        
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        filename : {"format": "json"},
    },
    "AUTOTHROTTLE_ENABLED": True
})

process.crawl(QuotesSpider1)
process.start()