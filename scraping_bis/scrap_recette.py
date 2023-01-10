import os
import json
import pandas as pd
import scrapy
import logging
from scrapy.utils.request import request_fingerprint
from scrapy.crawler import CrawlerProcess

# Récupération des hôtels
class QuotesSpider1(scrapy.Spider):
    name = "spider1"

    file = pd.read_csv('plats.csv')
    file = file["url"]
    liste_url = [element for element in file]
    start_urls = liste_url
    
    def parse(self, response):
        print(response)
        
        yield {
                "plat" : response.css('h1.SHRD__sc-10plygc-0.itJBWW::text').get(),
                "recette" : response.xpath('/html/head/meta[18]').extract(),    
                }
                                 
filename = "recettes_plus.json"

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