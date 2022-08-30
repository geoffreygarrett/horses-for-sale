import scrapy
from .utils import get_driver
import time 
# import By.XPATH
from selenium.webdriver.common.by import By

# set selenium logger to WARNING
import logging
logging.getLogger('selenium').setLevel(logging.WARNING)


class Gumtree(scrapy.Spider):
    name = 'gumtree2'
    x1 = "//*/div[@class='related-items']//div[contains(@class,'related-item')]"
    x2 = "//a[@class='icon-pagination-right']"
    
    allowed_domains = ['gumtree.co.za']
    start_urls = ['https://www.gumtree.co.za/s-horses-ponies/v1c9141p1?q=horses+for+sale&pr=10000,']
    base_url = 'https://www.gumtree.co.za'
    driver = get_driver()
    custom_settings = {
        # "DOWNLOAD_DELAY": 5,
        'ROBOTSTXT_OBEY': False,
        'ITEM_PIPELINES': {
            # 'horses.pipelines.GumtreePipeline': 1,
            # 'horses.pipelines.HorsesPipeline': 2,
            # 'horses.pipelines.MongoPipeline': 300,
        }
    } 
    # def __init__(self, *args, **kwargs):
    #     super(Gumtree, self).__init__(*args, **kwargs)
    #     self.driver = get_driver()

    # close driver on spider close
    def close(self, reason):
        self.driver.quit()
        super().close(reason)

    def parse(self, response):

        # if driver
        # if not self.driver:
        #     self.driver = get_driver()

        # get page with driver
        self.driver.get(response.url)

        # wait for page to load
        time.sleep(10)

        # save html 
        with open("gumtree_{}.html".format(time.time()), "w") as f:
            f.write(self.driver.page_source)
        # get listings

        # get links in self.x1 with driver
        links = self.driver.find_elements(By.XPATH, self.x1)

        # get "href" attributes
        # links = [ for link in links]
        
        print("links: ", len(links))

        for link in links:
            url = link.find_element(By.TAG_NAME, "a").get_attribute("href")
            print("url: ", url)
            yield scrapy.Request(url, callback=self.parse_detail)


        # for link in response.xpath(self.x1):
        #     url = self.base_url + link.extract()
        #     yield scrapy.Request(url, callback=self.parse_detail)

        # get next page link with driver
        next_page = self.driver.find_element(By.XPATH, self.x2)

        # get "href" attribute
        next_page = next_page.get_attribute('href')
        print("next_page: ", next_page)

        # next_page_url = response.xpath(self.x2).get()

        # if next_page_url == None:
        #     with open('gumtree2.html', 'wb') as f:
        #         f.write(response.body)

        yield scrapy.Request(next_page, callback=self.parse)
 
    def parse_detail(self, response):
        # https://docs.scrapy.org/en/latest/topics/dynamic-content.html#topics-javascript-rendering
        # need dynamic content. see link above

        yield {
            "link": response.url,
            # "name": response.xpath("//*/div[@class='m-y-0 h3']/h1/text()").get().strip(),
            # "details": dict(zipped),
            # "price": response.xpath("//*/div[@class='h3 m-t m-b-0 theme-text']/b/text()").get().strip(),
            # "images": [b.get() for b in response.xpath("//*/div[@class='col-md-6']//*/img/@src")][1:],
        }
