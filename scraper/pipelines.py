# Import necessary libraries
import sqlite3
from scrapy.exceptions import DropItem
from .items import CategoryItem, ProductItem
from scrapy.exceptions import NotConfigured


# Define the pipeline class
class SastodealscrapingPipeline:

    # Initialize the pipeline with the database name and a dictionary to store category IDs
    def __init__(self, db_path):
        self.db_path = db_path
        self.category_ids = {}

    # This method is called by Scrapy to create a pipeline instance
    @classmethod
    def from_crawler(cls, crawler):
        db_path = crawler.settings.get('DB_PATH')
        if not db_path:
            raise NotConfigured('DB_PATH setting is required')
        return cls(db_path)

    
    # This method is called when the spider is opened
    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.db_path)
        self.curr = self.conn.cursor()
        self.create_table()

    # This method is called when the spider is closed
    def close_spider(self, spider):
        self.conn.close()

    # This method creates the necessary tables in the database
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS categories_tb""")
        self.curr.execute('''CREATE TABLE categories_tb(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name text,
        product_count INTEGER,
        category_url text
        )''')
        self.curr.execute("""DROP TABLE IF EXISTS products_tb""")
        self.curr.execute('''CREATE TABLE products_tb(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name text,
                product_url text,
                product_price DECIMAL(10, 5),
                image_url text,
                category_name text,
                category_id INTEGER,
                FOREIGN KEY(category_id) REFERENCES categories_tb(id)
                )''')

    # This method is called for every item pipeline component
    def process_item(self, item, spider):
        if not item['category_name']:
            raise DropItem("Missing category_name in %s" % item)
        self.store_db(item)
        return item

    # This method stores the item in the database
    def store_db(self,item):
        if (isinstance(item, CategoryItem)):
            self.curr.execute("""INSERT INTO categories_tb (category_name, product_count, category_url) VALUES (?,?,?)""",(
            item['category_name'],
            item['product_count'],
            item['category_url']
        ))
            self.category_ids[item['category_name']] = self.curr.lastrowid
        elif isinstance(item, ProductItem):
            category_id = self.category_ids.get(item['category_name'])
            if category_id is not None:
                self.curr.execute("""INSERT INTO products_tb (product_name, product_url, product_price, image_url, category_name, category_id) VALUES (?,?,?,?,?,?)""",(
                    item['product_name'],
                    item['product_url'],
                    item['product_price'],
                    item['image_url'],
                    item['category_name'],
                    category_id
                ))
        self.conn.commit()

