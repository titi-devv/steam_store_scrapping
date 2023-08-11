from w3lib.html import remove_tags
import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def remove_html(review_summary):
    cleaned_review_summary = ''
    try:
        cleaned_review_summary = remove_tags(review_summary)
    except TypeError:
        cleaned_review_summary = 'No reviews'
    return cleaned_review_summary


def clean_discount_rate(discount_rate):
    if discount_rate:
        return discount_rate.lstrip('-')
    return discount_rate


def get_original_price(html_markup):
    original_price = ''
    selector_obj = scrapy.Selector(text=html_markup)
    div_with_discount = selector_obj.xpath(
        ".//div[contains(@class,'discount_original_price')]/text()").get()
    if div_with_discount:
        original_price = div_with_discount
    else:
        original_price = selector_obj.xpath(
            ".//div[contains(@class,'discount_final_price')]/text()").get()
    return original_price


def get_discounted_price(html_markup):
    original_price = ''
    selector_obj = scrapy.Selector(text=html_markup)
    div_with_discount = selector_obj.xpath(
        ".//div[contains(@class,'discount_original_price')]/text()").get()
    if div_with_discount:
        original_price = selector_obj.xpath(
            ".//div[contains(@class,'discount_final_price')]/text()").get()
    else:
        original_price = None
    return original_price


def get_platforms(one_class):
    platforms = []

    platform = one_class.split(' ')[-1]
    if platform == 'win':
        platforms.append('Windows')
    if platform == 'mac':
        platforms.append('Mac os')
    if platform == 'lin':
        platforms.append('Linux')
    if platform == 'vr_supported':
        platforms.append('VR Supported')
    return platforms


class SteamItem(scrapy.Item):
    game_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    img_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    game_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    release_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    platforms = scrapy.Field(
        input_processor=MapCompose(get_platforms)
    )
    reviews_summary = scrapy.Field(
        input_processor=MapCompose(remove_html),
        output_processor=TakeFirst()
    )

    original_price = scrapy.Field(
        input_processor=MapCompose(get_original_price),
        output_processor=TakeFirst()
    )
    discounted_price = scrapy.Field(
        input_processor=MapCompose(get_discounted_price),
        output_processor=TakeFirst()
    )
    discount_rate = scrapy.Field(
        input_processor=MapCompose(clean_discount_rate),
        output_processor=TakeFirst()
    )
