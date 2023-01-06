import os
import scrapy
import logging
from scrapy.utils.request import request_fingerprint
from scrapy.crawler import CrawlerProcess
import random

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
                if response.css('span') == 'TV1' :
                            "rouge" : response.css('span.TV1::text').getall(),
                        else :



                "rouge" : response.css('span.TV1::text').getall(),
                "blanc" : response.css('span.TV2::text').getall(),
                "rose" : response.css('span.TV3::text').getall(),
                "blanc_moelleux" : response.css('span.TV4::text').getall(),
                "blanc_effervescent" : response.css('span.TV5::text').getall(),
                "rose_effervescent" : response.css('span.TV6::text').getall(),
                "rouge_effervescent" : response.css('span.TV7::text').getall(),
                "autre" : response.css('span.TV99::text').getall(),
                }
                                 
filename = "test.json"

if filename in os.listdir():
        os.remove( filename)
        
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]

process = CrawlerProcess(settings = {
    'USER_AGENT': user_agent_list[random.randint(0, len(user_agent_list)-1)],
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        filename : {"format": "json"},
    },
    "AUTOTHROTTLE_ENABLED": True
})

process.crawl(QuotesSpider1)
process.start()


