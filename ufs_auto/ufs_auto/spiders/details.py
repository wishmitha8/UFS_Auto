import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from datetime import datetime

# Initialize a list to store scraped data
data_list = []

class DetailsSpider(scrapy.Spider):
    name = "project2"
    allowed_domains = ["ufsauto.com"]

    # Read the list of links from the CSV file
    links_csv_path = "output/links.csv"
    links_df = pd.read_csv(links_csv_path)
    links = links_df['Item Link'].values.tolist()

    def start_requests(self):
        for url in self.links:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        data = {
            'Stock No': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[1]/td[2]/text()').get(),
            'v_name': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[2]/h1/span/text()').get(),
            'price': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/div[2]/div[2]/div/text()').get(),
            'chassis': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[2]/td[2]/text()').get(),
            'Model': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[3]/td[2]/text()').get(),
            'Make':response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[4]/td[2]/text()').get(),
            'Boby type': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[5]/td[2]/text()').get(),
            'Transmission': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[6]/td[2]/text()').get(),
            'Model Year': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[7]/td[2]/text()').get(),
            'Mileage': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[8]/td[2]/text()').get(),
            'Location': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[1]/td[4]/text()').get(),
            'Drive': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[2]/td[4]/text()').get(),
            'Engine Size': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[3]/td[4]/text()').get(),
            'Steering': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[4]/td[4]/text()').get(),
            'Color': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[5]/td[4]/text()').get(),
            'Fuel': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[6]/td[4]/text()').get(),
            'Seats': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[7]/td[4]/text()').get(),
            'Doors': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[8]/td[4]/text()').get(),
            'Dimension': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[10]/td[2]/text()').get(),
            'Weight': response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[5]/div/table[1]/tbody/tr[11]/td[2]/text()').get(),
            'Scrap Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Source': 'ufsauto',
            'Link': response.url
        }

        data_list.append(data)

# Define a function to start the spider
process = CrawlerProcess()
process.crawl(DetailsSpider)
process.start()

# After crawling, create a DataFrame from the scraped data
df = pd.DataFrame(data_list)

# Save the DataFrame to a CSV file
df.to_csv('output/details.csv', index=False)
