import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["apple-market.ru"]
    start_urls = ["https://apple-market.ru/iphone/?page=1"]

    def parse(self, response):
        heads = response.xpath('//ul[@class="catalog-page__list"]/li')
        for head in heads:
            yield {

                'name': head.xpath('.//h3[@class="product__name"]/a/text()').get().strip(),
                'price': head.xpath('.//span[@class="product__price"]/text()').get().strip(),
                'photo': response.xpath('//a[@class="product__image-link"]/img/@src').get()
            }

        # Находим номер текущей страницы
        current_page = response.url.split('page=')[1]  # Убираем все до 'page='
        current_page = int(current_page)  # Преобразуем в целое число

        # Если текущая страница меньше 50, продолжаем извлечение
        if current_page < 50:
            next_page = current_page + 1  # Переход к следующей странице
            next_url = f"https://apple-market.ru/mac/?page={next_page}"
            yield scrapy.Request(next_url, callback=self.parse)  # Отправляем запрос на следующую страницу
