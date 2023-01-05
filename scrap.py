import os
import scrapy
import logging
from scrapy.utils.request import request_fingerprint
from scrapy.crawler import CrawlerProcess

# Récupération des hôtels
class QuotesSpider1(scrapy.Spider):
    name = "spider1"

    urls = []
    
    for i in range(1, 50):
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/aperitif-dinatoire/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/bouchee-ou-amuse-bouche/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/viande/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/poisson/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/pates-riz-semoule/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/oeufs/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/fruits-de-mer/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/dessert-au-chocolat/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/gateau/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/creme/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/dessert-glace/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/tarte/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/plat-vegetarien/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/entree-chaude/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/andouilette/{i}")
        urls.append(f"https://www.marmiton.org/recettes/index/categorie/abats/{i}")

    start_urls = urls 
    
    def parse(self, response):
        print(response)

        yield {
                "target" : response.css('h1.main-title::text').get(),
                "plat": response.css("h4.recipe-card__title::text").getall(), 
                "url": response.css("a.recipe-card-link::attr(href)").getall() 
                }
                                 
filename = "data.json"

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