import os
import scrapy
import logging
from scrapy.utils.request import request_fingerprint
from scrapy.crawler import CrawlerProcess

# Récupération des hôtels
class QuotesSpider1(scrapy.Spider):
    name = "spider1"

    target = ["Fromages", "Poulet", "Boeuf", "Abats", "Apéritif", "Charcuteries", "Desserts", "Fruits de mer", "Gibiers", "Légumes", "Pâtes", "Poissons", "Salades & crudités", "Lapin", "Oeuf", "Viandes blanches", "Soupes"]

    urls = []
    
    for i in target:
        urls.append(f"https://www.platsnetvins.com/accords-plats-mets-vins.php?plat={i}")
       
    start_urls = urls 
    
    def parse(self, response):
        print(response)

        yield {
                "target" : response.css('input#plat::attr(value)').extract(),
                "vin" : response.css('a.Accord::text').getall(), 
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