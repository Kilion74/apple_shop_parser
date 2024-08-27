import scrapy


class ExampleSpider(scrapy.Spider):
    name = "card_json"
    allowed_domains = ["apple-market.ru"]

    # start_urls = ["https://apple-market.ru/iphone/?page={}"]
    def start_requests(self):
        base_url = "https://apple-market.ru/mac/?page={}"
        for count in range(1, 26):
            yield scrapy.Request(url=base_url.format(count), callback=self.parse)

    def parse(self, response):
        # Извлекаем все карточки товаров из списка
        heads = response.xpath('//ul[@class="catalog-page__list"]/li')
        for head in heads:
            product_link = head.xpath('.//div[@class="product__preview"]/a/@href').get()
            # Генерируем полный URL для товара
            full_product_link = response.urljoin(product_link)

            # Отправляем запрос на страницу товара
            yield scrapy.Request(full_product_link, callback=self.parse_product)

    def parse_product(self, response):
        # Извлекаем данные о товаре более подробно
        product_data = {
            'name': response.xpath('.//h1[@class="product-review__info-title"]/text()').get().strip(),
            'price': response.xpath('//div[@class="product-review__buy-price"]/text()').get().strip(),
            'photo': response.xpath('.//img[@itemprop="contentUrl"]/@src').get(),
            'description': []
        }

        # Извлекаем каждый элемент описания и добавляем его в список.
        description_elements = response.xpath(
            '//tbody[@class="product-review__characteristics-list-container"]/tr')
        for element in description_elements:
            key = element.xpath('.//td[@class="product-review__characteristics-label"]/text()').get()
            value = element.xpath('.//td[@class="product-review__characteristics-value"]/text()').get()
            text = key + ': ' + value
            if text:
                product_data['description'].append(text.strip())

        yield product_data
