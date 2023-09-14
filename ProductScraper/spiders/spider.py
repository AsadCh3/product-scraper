import re
import scrapy

class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["hobartcorp.com"]
    start_urls = ["https://www.hobartcorp.com/products"]

    def parse(self, response):
        # body = response.body
        field_items = response.css('div.field-item.even')[:-1]
        field_items += response.css('div.field-item.odd')[:-1]
        field_items = field_items[1:]

        for item in field_items:
            path_url = item.css('a::attr(href)').extract()[0]
            url = f'https://www.hobartcorp.com{path_url}'

            yield scrapy.Request(
                url,
                callback=self.parse_hobartcorp
            )

    def parse_hobartcorp(self, response):
        field_items = response.css('div.field-item.even')
        field_items += response.css('div.field-item.odd')

        for item in field_items:
            path_url = item.css('a::attr(href)').extract()[0]

            if not 'hobartcorp' in path_url and 'products' in path_url:
                url = f'https://www.hobartcorp.com{path_url}'

                yield scrapy.Request(
                    url,
                    callback=self.parse_hobartcorp_produts
                )

    def parse_hobartcorp_produts(self, response):
        field_items = response.css('div.field-item.even')
        field_items += response.css('div.field-item.odd')

        for item in field_items:
            path_url = item.css('a::attr(href)').extract()[0]

            if not 'hobartcorp' in path_url and 'products' in path_url:
                url = f'https://www.hobartcorp.com{path_url}'

                yield scrapy.Request(
                    url,
                    callback=self.process_hobartcorp_products
                )

    def process_hobartcorp_products(self, response):
        product = response.css('h1::text').extract()[0]
        # model_2 = re.sub(r'[^a-zA-Z0-9]', '', product)
        yield {'product': product}

        # print(response.body)

                

        

