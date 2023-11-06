import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class DetailsSpider(scrapy.Spider):
    name = "ufs_auto"
    allowed_domains = ["ufsauto.com"]
    start_urls = ['https://ufsauto.com/make.html?p=1']

    custom_settings = {
        'LOG_FILE': 'log_page_links.log',
        'LOG_LEVEL': 'ERROR',
        'FEED_FORMAT': 'csv',  # Save data to CSV format
        'FEED_URI': 'page_links.csv',  # Output links to "page_links.csv"
        'FEED_OVERWRITE': True,
    }

    def parse(self, response):
        # Extract and yield all text within li elements

            li_values = response.xpath('//*[@id="narrow-by-list"]/div[1]/div[2]/ol/li/a/span/text()').getall()
            count=0

            for value in li_values:
               count=count+ int(value)
            page_count= round(count/15) +1

            page_links=[]
            for i in range (1,(page_count)+1):
                #'https://ufsauto.com/make.html?p={i}'
                url = f'https://ufsauto.com/make.html?p={i}'
                page_links.append(url)
            # Convert the list of page links to a DataFrame
            df = pd.DataFrame({"page_links": page_links})


        # Save the DataFrame to a CSV file
            df.to_csv('page_links.csv', index=False)



process = CrawlerProcess()
process.crawl(DetailsSpider)
process.start()
