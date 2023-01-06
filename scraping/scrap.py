import os
import scrapy
import logging
from scrapy.utils.request import request_fingerprint
from scrapy.crawler import CrawlerProcess

# Récupération des hôtels
class QuotesSpider1(scrapy.Spider):
    name = "spider1"

    urls = []
    target =["https://www.marmiton.org/recettes/recherche.aspx?aqt=Poulet","https://www.marmiton.org/recettes/recherche.aspx?aqt=viandes-blanche",
            "https://www.marmiton.org/recettes/recherche.aspx?aqt=oeufs","https://www.marmiton.org/recettes/recherche.aspx?aqt=lapin", "https://www.marmiton.org/recettes/recherche.aspx?aqt=poissons", 
            "https://www.marmiton.org/recettes/recherche.aspx?aqt=pâtes", "https://www.marmiton.org/recettes/recherche.aspx?aqt=Légumes", "https://www.marmiton.org/recettes/recherche.aspx?aqt=Gibiers", 
            "https://www.marmiton.org/recettes/recherche.aspx?aqt=Fruit-de-mer", "https://www.marmiton.org/recettes/recherche.aspx?aqt=Dessert",  
            "https://www.marmiton.org/recettes/recherche.aspx?aqt=Apéritif", "https://www.marmiton.org/recettes/recherche.aspx?aqt=Abats", "https://www.marmiton.org/recettes/recherche.aspx?aqt=Boeuf", 
            "https://www.marmiton.org/recettes/recherche.aspx?aqt=Soupes", "https://www.marmiton.org/recettes/recherche.aspx?aqt=Salades"]
    

    for i in target:
        urls.append()

    
       

    start_urls = urls 
    
    def parse(self, response):
        print(response)

        yield {
                "target" : response.css('span.MRTN__sc-16jp16z-1.gzsDhH::text').get(),
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