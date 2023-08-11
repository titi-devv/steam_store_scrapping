import json
import scrapy
from ..items import SteamItem
from w3lib.html import remove_tags
from scrapy.loader import ItemLoader


class BestSellingSpider(scrapy.Spider):
    name = "best_selling"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com/search/?filter=topsellers"]

    def start_requests(self):
        yield scrapy.Request(
            url='https://store.steampowered.com/search/results/?query&start=2000&count=50&dynamic_data=&sort_by=_ASC&supportedlang=french&snr=1_7_7_7000_7&filter=topsellers&infinite=1',
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'X-Prototype-Version': '1.7'
            },
            callback=self.parse,
            meta={
                'start': 0
            }
        )

    def get_platforms(self, list_classes):
        platforms = []
        for item in list_classes:
            platform = item.split(' ')[-1]
            if platform == 'win':
                platforms.append('Windows')
            if platform == 'mac':
                platforms.append('Mac os')
            if platform == 'lin':
                platforms.append('Linux')
            if platform == 'vr_supported':
                platforms.append('VR Supported')
        return platforms

    def remove_html(self, review_summary):
        cleaned_review_summary = ''
        try:
            cleaned_review_summary = remove_tags(review_summary)
        except TypeError:
            cleaned_review_summary = 'No reviews'
        return cleaned_review_summary

    def clean_discount_rate(self, discount_rate):
        if discount_rate:
            return discount_rate.lstrip('-')
        return discount_rate

    def get_original_price(self, selector_obj):
        original_price = ''
        div_with_discount = selector_obj.xpath(
            ".//div[contains(@class,'discount_original_price')]/text()").get()
        if div_with_discount:
            original_price = div_with_discount
        else:
            original_price = selector_obj.xpath(
                "normalize-space(.//div[contains(@class,'discount_final_price')]/text())").get()
        return original_price

    def get_discounted_price(self, selector_obj):
        original_price = ''
        div_with_discount = selector_obj.xpath(
            ".//div[contains(@class,'discount_original_price')]/text()").get()
        if div_with_discount:
            original_price = selector_obj.xpath(
                ".//div[contains(@class,'discount_final_price')]/text()").get()
        else:
            original_price = None
        return original_price

    def parse(self, response):
        resp = json.loads(response.body)
        html = resp.get('results_html')
        html_selector = scrapy.Selector(text=html)
        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(html)

        games = html_selector.xpath(
            "//a[contains(@class,'search_result_row ds_collapse_flag')]")
        for game in games:
            loader = ItemLoader(
                item=SteamItem(), selector=game, response=response)
            loader.add_xpath("game_url", ".//@href")

            loader.add_xpath('img_url', './/div[1]/img/@src')
            loader.add_xpath("game_name", ".//div/span[@class='title']/text()")
            loader.add_xpath(
                "release_date", './/div/div[@class="col search_released responsive_secondrow"]/text()')
            loader.add_xpath(
                "platforms", ".//span[contains(@class, 'platform_img') or (@class='vr_supported')]/@class")
            loader.add_xpath(
                "reviews_summary", './/span[contains(@class,"search_review_summary")]/@data-tooltip-html')
            loader.add_xpath(
                "original_price", './/div[contains(@class,"discount_block search_discount_block")]')
            loader.add_xpath(
                "discounted_price", './/div[contains(@class,"discount_block search_discount_block")]')
            loader.add_xpath(
                "discount_rate", './/div[contains(@class,"discount_pct")]/text()')
            yield loader.load_item()

            # steam_item['game_url'] = game.xpath('.//@href').get()
            # steam_item['img_url'] = game.xpath('.//div[1]/img/@src').get()
            # steam_item['game_name'] = game.xpath(
            #     ".//div/span[@class='title']/text()").get()
            # steam_item['release_date'] = game.xpath(
            #     './/div/div[@class="col search_released responsive_secondrow"]/text()').get()
            # steam_item['platforms'] = self.get_platforms(game.xpath(
            #     ".//span[contains(@class, 'platform_img') or (@class='vr_supported')]/@class").getall())

            # steam_item['reviews_summary'] = self.remove_html(game.xpath(
            #     './/span[contains(@class,"search_review_summary")]/@data-tooltip-html').get())
            # steam_item['original_price'] = self.get_original_price(game.xpath(
            #     './/div[contains(@class,"discount_block search_discount_block")]'))
            # steam_item['discounted_price'] = self.get_discounted_price(game.xpath(
            #     './/div[contains(@class,"discount_block search_discount_block")]'))
            # steam_item['discount_rate'] = self.clean_discount_rate(game.xpath(
            #     './/div[contains(@class,"discount_pct")]/text()').get())
            # yield steam_item

        current_start = response.meta['start']
        next_start = current_start + 50
        new_url = f"https://store.steampowered.com/search/results/?query&start={current_start}&count=50&dynamic_data=&sort_by=_ASC&supportedlang=french&snr=1_7_7_7000_7&filter=topsellers&infinite=1"
        if next_start <= 200:
            yield scrapy.Request(
                url=new_url,
                headers={
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-Prototype-Version': '1.7'
                },
                callback=self.parse,
                meta={
                    'start': next_start
                }
            )
