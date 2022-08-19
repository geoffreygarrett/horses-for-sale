import scrapy


class JunkMail(scrapy.Spider):
    name = 'junkmail'
    x1 = "//*/div[@class='col-md-4 col-sm-12']"
    x2 = "//*/ul[@class='pagination']/li/*//@href"
    
    allowed_domains = ['junkmail.co.za']
    start_urls = ['https://www.junkmail.co.za/pets/horses-and-ponies/pr10000']
    base_url = 'https://www.junkmail.co.za'
    custom_settings = {
        "DOWNLOAD_DELAY": 0.25,
        'ITEM_PIPELINES': {
            'horses.pipelines.JunkmailPipeline': 1,
            'horses.pipelines.HorsesPipeline': 2,
            'horses.pipelines.MongoPipeline': 300,
        }
    } 

    def parse(self, response):
        for link in response.xpath(self.x1):
            url = self.base_url + link.xpath('.//@href').get()
            yield scrapy.Request(url, callback=self.parse_detail)
        next_page_url = response.xpath(self.x2)[-1].extract()
        yield scrapy.Request(self.base_url + next_page_url, callback=self.parse)
 
    def parse_detail(self, response):
        details = response.xpath("//*/li[@class='list-group-item']")
        zipped = []
        for x in details:
            k = x.xpath(".//*/text()")[0].get()[:-1]
            try:
                v = x.xpath(".//*/text()")[1].get()
            except IndexError:
                v = None
            zipped.append((k,v))

        yield {
            "link": response.url,
            "name": response.xpath("//*/div[@class='m-y-0 h3']/h1/text()").get().strip(),
            "details": dict(zipped),
            "price": response.xpath("//*/div[@class='h3 m-t m-b-0 theme-text']/b/text()").get().strip(),
#             "price": response.xpath("//*/div[@class='pull-left']/*/h4/text()").get(),
#             "location": response.xpath("//*/div[@class='panel panel-default map-panel']/div[@class='panel-footer']//text()")[1].get().strip(),
#             "details": dict(
#                 zip([x.get()[:-1] for x in response.xpath("//*/div[@class='panel panel-default']//*/tr/th/text()")], [x.get() for x in response.xpath("//*/div[@class='panel panel-default']//*/tr/td/text()")]))
# ,
#             "listing_date": response.xpath("//*/h4[@class='ad_date text-right']//text()").get(),
#             "ref": response.xpath("//*/div[@class='panel panel-default']//*/h4[@class='text-muted text-right']//text()").get().strip(),
            "images": [b.get() for b in response.xpath("//*/div[@class='col-md-6']//*/img/@src")],
        }
