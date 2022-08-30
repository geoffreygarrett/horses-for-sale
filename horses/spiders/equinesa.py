import scrapy


class EquineSASpider(scrapy.Spider):
    x1 = "//*/div[@class='col-md-8']/div[@class='list-group excl']/a[@class='list-group-item']"
    x2 = "//*/ul[@class='pagination']/li/*//@href"

    name = 'equinesa'
    allowed_domains = ['equinesa.net']
    start_urls = ['https://secure.equinesa.net/horses-for-sale/listings/all']
    base_url = 'https://secure.equinesa.net'
    custom_settings = {
        "DOWNLOAD_DELAY": 0.25,
        'ITEM_PIPELINES': {
            'horses.pipelines.EquinesaPipeline': 1,
            'horses.pipelines.HorsesPipeline': 2,
            'horses.pipelines.MongoPipeline': 300,
        }
    }

    sitemap_rules = [
        (r'/horses-for-sale/listings/all', 'parse'),
        (r'/horses-for-sale/detail/', 'parse_detail'),
    ]

    def parse(self, response):
        for link in response.xpath(self.x1):
            url = self.base_url + link.xpath('.//@href').get()
            yield scrapy.Request(url,callback=self.parse_detail)
        next_page_url = response.xpath(self.x2)[-1].extract()
        yield scrapy.Request(next_page_url, callback=self.parse)
 
    def parse_detail(self, response):

        yield {
            "link": response.url,
            "name": response.xpath("//*/div/h3/text()")[0].get().strip(),
            "price": response.xpath("//*/div[@class='pull-left']/*/h4/text()").get(),
            "location": response.xpath("//*/div[@class='panel panel-default map-panel']/div[@class='panel-footer']//text()")[1].get().strip(),
            "details": dict(
                zip([x.get()[:-1] for x in response.xpath("//*/div[@class='panel panel-default']//*/tr/th/text()")], [x.get() for x in response.xpath("//*/div[@class='panel panel-default']//*/tr/td/text()")]))
,
            "listing_date": response.xpath("//*/h4[@class='ad_date text-right']//text()").get(),
            "ref": response.xpath("//*/div[@class='panel panel-default']//*/h4[@class='text-muted text-right']//text()").get().strip(),
            "images": list(filter(lambda x: '/uploads/' in x, [self.base_url + b.get() for b in response.xpath("//*/div[@class='visible-xs text-center']//*/img/@src")])),
        }
