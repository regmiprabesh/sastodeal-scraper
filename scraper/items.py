# Import the scrapy library
import scrapy

class SastodealscrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# Define a class for category items that inherits from the base item
class CategoryItem(scrapy.Item):
    # Each category has an id, name, product count, and URL
    id = scrapy.Field()
    category_name = scrapy.Field()
    product_count = scrapy.Field()
    category_url = scrapy.Field()

# Define a class for product items that inherits from the base item
class ProductItem(scrapy.Item):
    # Each product has an id, name, URL, price, image URL, category name, and category id
    id = scrapy.Field()
    product_name = scrapy.Field()
    product_url = scrapy.Field()
    product_price = scrapy.Field()
    image_url = scrapy.Field()
    category_name = scrapy.Field()
    category_id = scrapy.Field()