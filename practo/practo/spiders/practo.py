import scrapy
from ..items import PractoItem

class practoSpider(scrapy.Spider):
    name = "practo"
    page_number = 2
    start_urls = [
        "https://www.practo.com/search?results_type=doctor&q=%5B%7B%22word%22%3A%22diabetologist%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=Bangalore",
        "https://www.practo.com/search?results_type=doctor&q=%5B%7B%22word%22%3A%22endocrinologist%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=bangalore"
            ]
    def parse(self, response):
        items = PractoItem()

        doctor_name = response.css(".doctor-name::text").extract()
        specialization = response.css(".u-d-inline span::text").extract()
        experience = response.css(".uv2-spacer--xs-top div::text").extract()
        fees = response.css(".uv2-spacer--xs-top span span::text").extract()

        items["doctor_name"] = doctor_name
        items["specialization"] = specialization
        items["experience"] = experience
        items["fees"] = fees
        yield (items)

        next_page = "https://www.practo.com/search?results_type=doctor&q=%5B%7B%22word%22%3A%22diabetologist%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=Bangalore&page="+ str(practoSpider.page_number)
        next_page1 = "https://www.practo.com/search?results_type=doctor&q=%5B%7B%22word%22%3A%22endocrinologist%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=bangalore&page="+ str(practoSpider.page_number)
        if practoSpider.page_number <= 3:
            practoSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

        if practoSpider.page_number <= 5:
            practoSpider.page_number += 1
            yield response.follow(next_page1, callback=self.parse)