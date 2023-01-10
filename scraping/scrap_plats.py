import os
import scrapy
import logging
from scrapy.utils.request import request_fingerprint
from scrapy.crawler import CrawlerProcess

# Récupération des hôtels
class QuotesSpider1(scrapy.Spider):
    name = "spider1"

    liste_urls = []
    
    for i in range(1,100):
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/creme/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/dessert-glace/{i}"),	
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/dessert-glace/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/tarte/{i}"),	        
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/tarte/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/plat-vegetarien/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/andouilette/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/abats/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/pates-riz-semoule/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/soupe/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/viande/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/oeufs/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/poisson/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/plat-vegetarien/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/autres-crudites/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/fruits-de-mer/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/terrine-pate/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/aperitif-dinatoire/{i}"),
        liste_urls.append(f"https://www.marmiton.org/recettes/index/categorie/bouchee-ou-amuse-bouche/{i}")

    start_urls = liste_urls 
    
    def parse(self, response):
        print(response)

        yield {
                "target" : response.css('h1.main-title::text').get(),
                "plat": response.css("h4.recipe-card__title::text").getall(), 
                "url": response.css("a.recipe-card-link::attr(href)").getall() 
                }
                                 
filename = "plats.json"

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