import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess

class DetailsSpider(scrapy.Spider):
    name = "ufs_auto"
    allowed_domains = ["ufsauto.com"]

    start_urls = ['https://ufsauto.com/make.html?p=1']

    custom_settings = {
        'LOG_FILE': 'log_page_links.log',
        'LOG_LEVEL': 'ERROR',
    }

    def parse(self, response):
        page_links = [response.url]

        # Determine the page number from the URL
        page_number = response.url.split('=')[-1]

        # Use different XPath based on the page number
        if page_number == '1':
            next_page_xpath = '//*[@id="layer-product-list"]/div[3]/div[3]/ul/li[6]/a/@href'
        else:
            next_page_xpath = '//*[@id="layer-product-list"]/div[3]/div[3]/ul/li[7]/a/@href'

        # Extract the next page link using the provided XPath
        next_page_link = response.xpath(next_page_xpath).extract_first()

        if next_page_link:
            yield scrapy.Request(
                url=next_page_link,
                callback=self.parse
            )

        df = pd.DataFrame({"page_links": page_links})
        # Append data to a CSV file
        df.to_csv('page_links.csv', mode='a', index=False, header=False)

process = CrawlerProcess()
process.crawl(DetailsSpider)
process.start()
