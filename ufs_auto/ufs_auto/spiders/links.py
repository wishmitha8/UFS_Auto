import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess

class DetailsSpider(scrapy.Spider):
    name = "project1"

    allowed_domains = ["ufsauto.com"]

    # Assuming that your CSV file has only one column (no header) containing the links
    lnks = pd.read_csv("page_links.csv", header=None)
    lks = lnks.iloc[:, 0].values.tolist()

    custom_settings = {
        'LOG_FILE': 'log_link.log',
        'LOG_LEVEL': 'ERROR',
        'FEED_FORMAT': 'csv',  # Save data to CSV format
        'FEED_URI': 'output/links.csv',  # Output links to "links.csv"
        'FEED_OVERWRITE': True,
    }

    def start_requests(self):
        for url in self.lks:
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        # Extract all the links within the element with id "layer-product-list"
        item_links = response.xpath('//*[@id="layer-product-list"]/div[2]/ol//a/@href').getall()
        unique_item_links = list(set(item_links))
        unique_item_links = [link for link in unique_item_links if 'php echo $_product->getProductUrl()' not in link]



        for link in unique_item_links:
            yield {
                'Item Link': response.urljoin(link)
            }

process = CrawlerProcess()
process.crawl(DetailsSpider)
process.start()
