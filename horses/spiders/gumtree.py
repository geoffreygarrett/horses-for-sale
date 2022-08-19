import scrapy


class Gumtree(scrapy.Spider):
    name = 'gumtree'
    x1 = "//*/div[@class='related-items']//div[contains(@class,'related-item')]//@href"
    x2 = "//a[@class='icon-pagination-right']//@href"
    
    allowed_domains = ['gumtree.co.za']
    start_urls = ['https://www.gumtree.co.za/s-horses-ponies/v1c9141p1?q=horses+for+sale&pr=10000,']
    base_url = 'https://www.gumtree.co.za'
    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        'ROBOTSTXT_OBEY': False,
        'ITEM_PIPELINES': {
            # 'horses.pipelines.GumtreePipeline': 1,
            # 'horses.pipelines.HorsesPipeline': 2,
            # 'horses.pipelines.MongoPipeline': 300,
        }
    } 

    def parse(self, response):
        # save html
        with open('gumtree.html', 'wb') as f:
            f.write(response.body)
            # raise Exception('done')
        
        # print("M!", response.xpath(self.x1))
        for link in response.xpath(self.x1):
            url = self.base_url + link.extract()
            yield scrapy.Request(url, callback=self.parse_detail)
        next_page_url = response.xpath(self.x2).get()
        print("UUUUU2 ---- ",next_page_url)
        if next_page_url == None:
            with open('gumtree2.html', 'wb') as f:
                f.write(response.body)
        yield scrapy.Request(self.base_url + next_page_url, callback=self.parse)
 
    def parse_detail(self, response):


        yield {
            "link": response.url,
            # "name": response.xpath("//*/div[@class='m-y-0 h3']/h1/text()").get().strip(),
            # "details": dict(zipped),
            # "price": response.xpath("//*/div[@class='h3 m-t m-b-0 theme-text']/b/text()").get().strip(),
            # "images": [b.get() for b in response.xpath("//*/div[@class='col-md-6']//*/img/@src")][1:],
        }
