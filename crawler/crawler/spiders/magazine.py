import scrapy
from crawler.items import Product

class MagazineSpider(scrapy.Spider):
    name = "magazine"

    def start_requests(self):
        urls = [
            'https://www.magazineluiza.com.br/notebook/informatica/s/in/note/',
            'https://www.magazineluiza.com.br/geladeira-refrigerador/eletrodomesticos/s/ed/refr/',
            'https://www.magazineluiza.com.br/celulares-e-smartphones/l/te/'
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
        ul_main = response.xpath('//ul[@role="main"]/a')

        hrefs = [a.xpath('@href').extract_first() for a in ul_main]

        for href in hrefs:
            yield scrapy.Request(url=href, callback=self.parse_product)

    def parse_product(self, response):
        # Use Product Item
        # Parse the product title, category and description
        # Product()
        product = Product()
        pass