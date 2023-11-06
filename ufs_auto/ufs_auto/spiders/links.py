import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess

# Initialize a global DataFrame to store the data
global_df = pd.DataFrame(columns=["Item Link"])

class DetailsSpider(scrapy.Spider):
    name = "project1"
    allowed_domains = ["ufsauto.com"]

    # Read the CSV file, skipping the header
    lnks = pd.read_csv("page_links.csv", header=0, names=["page_links"])

    # Extract the links from the first column
    lks = lnks["page_links"].values.tolist()

    def start_requests(self):
        for url in self.lks:
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        # Initialize a list to store item links for this page
        item_links = []

        # Extract all the links within the element with id "layer-product-list"
        item_links = response.xpath('//*[@id="layer-product-list"]/div[2]/ol//a/@href').getall()
        unique_item_links = list(set(item_links))
        unique_item_links = [link for link in unique_item_links if 'php echo $_product->getProductUrl()' not in link]

        for link in unique_item_links:
            # Append the unique_item_links to the global DataFrame
            global_df.loc[len(global_df)] = [response.urljoin(link)]

process = CrawlerProcess()
process.crawl(DetailsSpider)
process.start()

# Save the global DataFrame to a CSV file
global_df = global_df.drop_duplicates()
global_df.to_csv('output/links.csv', index=False)
