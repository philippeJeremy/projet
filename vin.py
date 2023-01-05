import os
import scrapy
import logging
from scrapy.utils.request import request_fingerprint
from scrapy.crawler import CrawlerProcess

# Récupération des hôtels
class QuotesSpider1(scrapy.Spider):
    name = "spider1"

    target = ["Fromage", "Poulet", "Boeuf"]

    urls = []
    
    for i in target:
        urls.append(f"https://www.platsnetvins.com/accords-plats-mets-vins.php?plat={i}")
       

    start_urls = urls 
    
    def parse(self, response):
        print(response)
        keys = response.css('div.col c2_of_3_RA')
        for key in keys:
            yield {
                "vin" : key.css('div.Accord::text').get(),
                "plat": key.css('//*[@class="card cardresuA"]/div/div[3]/span/text()').get(), 
                # "url": key.css("a.recipe-card-link::attr(href)").getall() 
                }
                                 
filename = "vin.json"

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