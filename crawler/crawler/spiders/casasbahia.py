import scrapy
from crawler.items import Product
import logging
import re

class_maping = {'celulares e smartphones': 'Celular e Smartphone', 'ar-condicionado e aquecedores':'Ar-Condicionado',
                'fogão': 'Fogão',
                'geladeira / refrigerador': 'Geladeira / Refrigerador',
                'guarda-roupa': 'Guarda-Roupa / Roupeiro', 'lava e seca': 'Lava e Seca', 
                'monitor gamer': 'Monitores',
                'máquina de lavar': 'Máquina de Lavar',
                'notebook': 'Notebook', 'smart tv': 'Smart TV'}

page_num_re = re.compile(r'/*paginaAtual=(\d+)', re.I | re.M | re.U)

class CasasBahiaSpider(scrapy.Spider):
    name = 'casasbahia'  # unique key

    def start_requests(self):
        urls = [
            'https://www.americanas.com.br/categoria/celulares-e-smartphones?chave=pfm_hm_tt_1_0_celulares',
            'https://www.americanas.com.br/categoria/moveis/guarda-roupa',
            'https://www.americanas.com.br/categoria/ar-condicionado-e-aquecedores?chave=pfm_hm_tt_1_0_arcondicionado',
            'https://www.americanas.com.br/categoria/informatica/notebook?chave=pfm_hm_tt_1_0_info',
            'https://www.americanas.com.br/categoria/eletrodomesticos/maquina-de-lavar',
            'https://www.americanas.com.br/categoria/eletrodomesticos/lava-e-seca',
            'https://www.americanas.com.br/categoria/pc-gamer/perifericos-gamers/monitor-gamer',
            'https://www.americanas.com.br/categoria/tv-e-home-theater/tv/smart-tv',
            'https://www.americanas.com.br/categoria/eletrodomesticos/geladeira-refrigerador',
            'https://www.americanas.com.br/categoria/eletrodomesticos/fogao'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        """Get all pages from the current category
        and follow the links
        """
        print(response.url)
        
        yield None
        #current_url = response.url
        #for i in range(1, number_of_pages + 1):
        #    yield scrapy.Request(url='%s?page=%d' % (current_url, i), callback=self.parse_page)

    def parse_page(self, response):
        """Extract all product links from the current page
        and sends a request to parse the product
        """
        hrefs = response.xpath('//ul[@role="main"]/a/@href').extract()

        category = response.xpath(
            '//ol[@data-css-rczytq=""]/li[last()]/a/text()').extract_first()

        for href in hrefs:
            yield scrapy.Request(url=href, callback=self.parse_product, meta={"category": category})

    def parse_product(self, response):
        # Use Product Item
        # Parse the product title, category and description
        # Product()

        product = Product()

        # Getting title
        title = response.xpath(
            '//h1[@class="header-product__title"]/text()').extract_first()
        if(title == None):
            title = response.xpath(
                '//h1[@class="header-product__title--unavailable"]/text()').extract_first()
        product["title"] = title

        # Getting Category
        category = response.meta['category']
        product["category"] = category

        # Getting Description
        path_description = response.xpath(
            '//div[@id="anchor-description"]/div/text()').extract()
        for i in path_description:
            if(len(i) > 30):
                description = i
        product["description"] = description

        yield product
