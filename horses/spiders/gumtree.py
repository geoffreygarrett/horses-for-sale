import scrapy
from scrapy_playwright.page import PageMethod


class Gumtree(scrapy.Spider):
    name = 'gumtree'
    allowed_domains = ['gumtree.co.za']
    start_urls = [
        'https://www.gumtree.co.za/s-horses-ponies/v1c9141p1?q=horses+for+sale&pr=10000,']

    custom_settings = {
        # "DOWNLOAD_DELAY": 0.25,
        'ROBOTSTXT_OBEY': False,
        'ITEM_PIPELINES': {
            'horses.pipelines.GumtreePipeline': 1,
            'horses.pipelines.HorsesPipeline': 2,
            'horses.pipelines.MongoPipeline': 300,
        },

    }
    meta_1 = dict(
        playwright=True,
        playwright_include_page=True,
    )
    

    meta_2 = dict(
        playwright_page_methods=[
                        PageMethod("wait_for_timeout", 10000),

            # PageMethod("wait_for_selector", "button.confirm"),
            # PageMethod("click", "button.confirm"),
            # PageMethod("reload"),

            # PageMethod("wait_for_selector", "button.enable"),
            # PageMethod("click", "button.confirm"),


            # PageMethod(
            #     "evaluate",
            #     "document.querySelectorAll('button.confirm')[0].click()"),

            # PageMethod(
            #     "evaluate",
            #     "document.querySelectorAll('button.enable')[0].click()"),
            # PageMethod("click", "button.enable"),
            # PageMethod("wait_for_event", "networkidle")
            # PageMethod("reload"),
            # PageMethod("on", "domcontentloaded", lambda: print("domcontentloaded")),
            # PageMethod(
            #     "evaluate",
            #     "document.querySelectorAll('button.enable')[0].click()"),
            # # PageMethod("wait_for_selector", "a.related-ad-title"),
        ],
        )

    custom_settings.update(**dict(
        PLAYWRIGHT_LAUNCH_OPTIONS={"headless": True},
        DOWNLOAD_HANDLERS={
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        TWISTED_REACTOR="twisted.internet.asyncioreactor.AsyncioSelectorReactor"

    ))

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={**self.meta_1, "playwright_context": "start", "cookiejar":i}
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        # await page.screenshot(
        #     path=f"{response.url.split('/')[-1][:-1].split('?')[0]}.png",
        #     full_page=True)

        # screenshot contains the image's bytes
        for item in response.xpath(
                "//*/div[@class='related-items']//div[contains(@class,'related-item')]//@href"):
            # print('url item: ',response.urljoin(item.get()))
            yield scrapy.Request(
                url=response.urljoin(item.get()),
                callback=self.parse_detail,
                meta={**self.meta_1, "cookiejar": response.meta["cookiejar"],
                      "playwright_context": "detail",
                      "playwright_page_methods": [
                                                  PageMethod("wait_for_load_state", "load"),

                      ]}
            )

        # # save page as html
        # with open("{}.html".format(
        #         response.url.split('/')[-1][:-1].split("?")[0]), "w") as f:
        #     f.write(response.text)

        next_page_url = response.xpath(
            "//a[@class='icon-pagination-right']/@href")
        # print('url next: ',response.urljoin(next_page_url.get()))

        yield scrapy.Request(
            url=response.urljoin(next_page_url.get()),
            callback=self.parse,
            meta=dict(**self.meta_1,
                      cookiejar=response.meta["cookiejar"],
                      playwright_page_methods=[
                          PageMethod("wait_for_selector", "a.icon-pagination-right"),
                          PageMethod("click", "a.icon-pagination-right"),
                      ],
                      playwright_context="parse"),
        )

    async def parse_detail(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        # horse_item = HorseItemL0()
        # horse_item["link"] = response.url
        yield {'link': response.url,
        'price': response.xpath("//*/div[@class='vip-summary']//span[@class='value wrapper']//span[@class='ad-price']/text()").get().replace("\n", "").strip(),
        'name':  response.css("div.title *::text").get(),
        'details': {
            'description': response.css("div.revip-description *::text").getall(),
            'location': "".join(response.css("div.location *::text").getall()),
            'images': list(filter(lambda x: "https" in x, response.xpath("//*/div[@class='gallery-area']//img/@src").getall())),
            'creation_date': response.css("span.creation-date *::text").get(),
            'views':  response.css("span.view-count *::text").get(),
        }
        }

        # yield {
        #     "link": response.url,
        #     # "name": response.xpath("//*/div[@class='m-y-0 h3']/h1/text()").get().strip(),
        #     # "details": dict(zipped),
        #     # "price": response.xpath("//*/div[@class='h3 m-t m-b-0 theme-text']/b/text()").get().strip(),
        #     # "images": [b.get() for b in response.xpath("//*/div[@class='col-md-6']//*/img/@src")][1:],
        # }
