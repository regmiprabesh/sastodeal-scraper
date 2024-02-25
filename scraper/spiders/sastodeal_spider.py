# Import the necessary libraries
import scrapy
from ..items import CategoryItem
from ..items import ProductItem
from scrapy_playwright.page import PageMethod
import re
from scrapy.utils.project import get_project_settings

# Define the spider class
class SastodealSpider(scrapy.Spider):

    #Define name of spider
    name = "sastodeal_spider"

    # Get the URL to start scraping from
    def __init__(self, *args, **kwargs):
        super(SastodealSpider, self).__init__(*args, **kwargs)
        settings = get_project_settings()
        self.website_url = settings.get('WEBSITE_URL')

    def start_requests(self):
        yield scrapy.Request(url=self.website_url, callback=self.parse)

    # Define the parse method that will be called to process the response of each request
    def parse(self, response):
        # Select the categories from the response
        categories_selector = response.css("div.filter-options-content > .items .item")
        #Initialize empty category item
        categories = CategoryItem()
        #Loop through categories
        for category in categories_selector:
            # Extract the category details
            category_name = category.css("a::Text").extract()
            product_count = category.css("span.count::Text").extract()
            category_url = category.css("a::attr('href')").extract()

            # Store the extracted data in the category item
            categories['category_name'] = category_name[0].strip()
            categories['product_count'] = int(product_count[0].strip())
            categories['category_url'] = category_url[0]
            
            # Yield the category item and a new request to parse the category
            yield categories
            #Go through every category page to scrape their product
            yield scrapy.Request(category_url[0],self.parse_category,cb_kwargs={"category_name": category_name},meta=dict(playwright = True,playwright_include_page = True,playwright_page_coroutines = [PageMethod('wait_for_selector','span.product-type-simple-price')]))
 
    # Define the method to parse a category    
    async def parse_category(self, response,category_name):
        # Select the products from the response
        products_selector = response.css("li.product-item")
        #Initialize empty product item
        products = ProductItem()
        #Loop through products in current page
        for product in products_selector:
            # Extract the product details
            product_name = product.css("a.product-item-link::Text").extract()
            product_url = product.css("a.product-item-link::attr('href')").extract()
            product_price = product.css("span.product-type-simple-price::Text").extract()
            image_url = product.css("span.product-image-wrapper img::attr('src')").extract()
            # Store the extracted data in the product item
            products['product_name'] = product_name[0].strip()
            products['product_url'] = product_url[0]
            #Convert the string to number before storing the price
            products['product_price'] =  float(re.sub(r'[^0-9.]', '',product_price[0].strip()))
            products['image_url'] = image_url[0]
            products['category_name'] = category_name[0].strip()
            # Yield the product item
            yield products
        # Get the URL of the next page
        next_page = response.css('a.next::attr(href)').get()
        # If there is a next page, yield a new request to parse it
        if next_page is not None:
            yield response.follow(next_page, callback= self.parse_category,cb_kwargs={"category_name": category_name},meta=dict(playwright = True,playwright_include_page = True,playwright_page_coroutines = [PageMethod('wait_for_selector','span.product-type-simple-price')]))