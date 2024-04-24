from datetime import datetime
import scrapy
from scrapy.crawler import CrawlerProcess
import pyairtable


class TheforgespiderSpider(scrapy.Spider):
    name = "theforgespider"
    start_urls = ["https://theforge.mcmaster.ca/pitchcompetition/"]

    def parse(self, response):
        items = {}
        items['year'] = '2023'

        winner_businesses = response.css('h3.wp-block-heading::text').getall()

        columns = ['winner business', '2nd place business', '3rd place business', '4th place business']

        for i, winner_business in enumerate(winner_businesses):
            business_name = winner_business.split(':')[-1].strip()
            column_name = columns[i] if i < len(columns) else f'{i + 1}th place business'
            items[column_name] = business_name

        winner_participant_elements = response.css('h4.wp-block-heading')

        columns = ['winner participants', '2nd place participants', '3rd place participants', '4th place participants']

        for i, column_name in enumerate(columns):
            if i >= len(winner_participant_elements):
                break

            text = winner_participant_elements[i].css('::text').get()

            participant_text = text.split(":")[-1].strip()
            items[column_name] = participant_text

            items['lastupdate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield(items)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(TheforgespiderSpider)
    process.start()
