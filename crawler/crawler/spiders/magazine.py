import scrapy
from crawler.items import Product
import logging

class MagazineSpider(scrapy.Spider):
    name = "magazine" # unique key

    def start_requests(self):
        urls = [
            'https://www.magazineluiza.com.br/notebook/informatica/s/in/note/',
            'https://www.magazineluiza.com.br/geladeira-refrigerador/eletrodomesticos/s/ed/refr/',
            'https://www.magazineluiza.com.br/celulares-e-smartphones/l/te/',
            'https://www.magazineluiza.com.br/guarda-roupa-roupeiro/moveis/s/mo/guro/',
            'https://www.magazineluiza.com.br/fogao/eletrodomesticos/s/ed/fogo/',
            'https://www.magazineluiza.com.br/ar-condicionado/ar-e-ventilacao/s/ar/arar/',  
            'https://www.magazineluiza.com.br/monitores/informatica/s/in/mlcd/',
            'https://www.magazineluiza.com.br/smart-tv/tv-e-video/s/et/elit/',
            'https://www.magazineluiza.com.br/lava-e-seca/eletrodomesticos/s/ed/ela1/',
            'https://www.magazineluiza.com.br/maquina-de-lavar/eletrodomesticos/s/ed/lava/'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        """Get all pages from the current category
        and follow the links
        """
        number_of_pages = response.xpath('//ul[@class="css-9j990n"]/li[9]/a/@aria-label').extract_first()
        # Returns: Page %d
        number_of_pages = int(number_of_pages.split(' ')[1])

        current_url = response.url
        for i in range(1, number_of_pages + 1):
            yield scrapy.Request(url='%s?page=%d' % (current_url, i), callback=self.parse_page)

    def parse_page(self, response):
        """Extract all product links from the current page
        and sends a request to parse the product
        """
        hrefs = response.xpath('//ul[@role="main"]/a/@href').extract()

        category = response.xpath('//ol[@data-css-rczytq=""]/li[last()]/a/text()').extract_first()

        for href in hrefs:
            yield scrapy.Request(url=href, callback=self.parse_product, meta={"category":category})

    def parse_product(self, response):
        # Use Product Item
        # Parse the product title, category and description
        # Product()
        
        product = Product()
        
        # Getting title
        title = response.xpath('//h1[@class="header-product__title"]/text()').extract_first()
        if(title == None):
            title = response.xpath('//h1[@class="header-product__title--unavailable"]/text()').extract_first()
        product["title"] = title

        # Getting Category
        category = response.meta['category']
        product["category"] = category

        # Getting Description
        path_description = response.xpath('//div[@id="anchor-description"]/div/text()').extract()
        for i in path_description:
            if(len(i) > 30):
                description = i
        product["description"] = description
    
        yield product