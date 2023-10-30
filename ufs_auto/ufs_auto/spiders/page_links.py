import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess

class DetailsSpider(scrapy.Spider):
    name = "ufs_auto"
    allowed_domains = ["ufsauto.com"]

    start_urls = ['https://ufsauto.com/make.html?p=1']

    # Define an empty list to store page links
    page_links = []

    custom_settings = {
        'LOG_FILE': 'log_page_links.log',
        'LOG_LEVEL': 'ERROR',
        'FEED_FORMAT': 'csv',  # Save data to CSV format
        'FEED_URI': 'page_links.csv',  # Output links to "page_links.csv"
        'FEED_OVERWRITE': True,
    }

    def parse(self, response):
        # Append the current page link to the list
        self.page_links.append(response.url)

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

    def closed(self, reason):
        # Convert the list of page links to a DataFrame
        df = pd.DataFrame({"page_links": self.page_links})

        # Save the DataFrame to a CSV file
        df.to_csv('page_links.csv', index=False)

process = CrawlerProcess()
process.crawl(DetailsSpider)
process.start()
