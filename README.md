# SastoDeal Liquor Scraper

This is a python based web scraping application that collects data about all liquor products and their categories from SastoDeal. The scraper is built using the Scrapy framework and stores the scraped data in an SQLite database.
It uses the Playwright package to handle JavaScript loaded websites and the Scrapy-User-Agents package to rotate user agents for each request.


## Installation

  1. Clone this repository to your local machine:
 
 ```bash
git clone https://github.com/<username>/<repository-name>.git
 ```

2. Open your terminal and navigate to the project directory:

```bash
cd sastodealscraping
```
3. Create a viertual environment for the project using venv:

```bash
python -m venv environment
```
4. Activate the virtual environment

```bash
source environment/bin/activate
```

5. Install the required Python packages. 
```bash
pip install -r requirements.txt
```

## Project Structure

The project has the following structure:
```
sastodealscraping/
│
├── scraper/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   │
│   └── spiders/
│       ├── __init__.py
│       └── sastodeal_spider.py
│
├── data/
│   ├── sastodeal.db
│
├── scrapy.cfg
│
└── requirements.txt

```
-   `scraper/`: This directory is where code related to scraping and settings related to scraping is kept.
-   `items.py`: This file contains the item classes for this project. These are custom Python dicts.
-   `pipelines.py`: This file is used to define the pipelines for this project. Pipelines are used for processing the items once they have been scraped.
-   `settings.py`: This file is used to configure the Scrapy project.
-   `spiders/`: This directory is where spiders kept.
-   `sastodeal_spider.py`: This is the spider that scrapes the SastoDeal website.
-   `scrapy.cfg`: This is the project configuration file. It contains settings for deploying the project.
-   `data/`: This directory is where database is kept.
-   `sastodeal.db`: This is the sqlite database file where data is stored after scraping
-   `requirements.txt`: This file lists the Python dependencies for this project.

## Usage

To start the scraper, navigate to the project directory and run the following command:
```bash
scrapy crawl sastodeal_spider
```
This will start the scraper and begin storing data in the SQLite database.


## Items

The items scraped by this project are defined in the `items.py` file. They are:

- `CategoryItem`: Contains information about a product category. Fields: `id`, `category_name`, `product_count`, `category_url`.
- `ProductItem`: Contains information about a product. Fields: `id`, `product_name`, `product_url`, `product_price`, `image_url`, `category_name`, `category_id`.

## Spiders

This project contains one spider and you can list them using the `scrapy list` command:

- `sastodeal_spider`: This spider scrapes the liquor section of the SastoDeal website.

## Pipeline

The pipeline for this project is defined in the `pipelines.py` file. It includes the following classes:

- `SastodealscrapingPipeline`: This pipeline processes the items scraped by the spiders. It performs the following tasks:
  - Opens a connection to an SQLite database at the start of the spider and closes it when the spider finishes.
  - Creates the necessary tables in the database.
  - Processes each item, checks if it has a `category_name`, and stores it in the database.

The pipeline uses SQLite to store the scraped data. The database name is specified in the Scrapy settings.

## Data Schema

The data in this project is organized into two main tables: `categories_tb` and `products_tb`.

1. `categories_tb`: This table stores information about each product category. It has the following fields:
    - `id`: An auto-incrementing integer that serves as the primary key.
    - `category_name`: The name of the product category.
    - `product_count`: The number of products in this category.
    - `category_url`: The URL of the category page.

2. `products_tb`: This table stores information about each product. It has the following fields:
    - `id`: An auto-incrementing integer that serves as the primary key.
    - `product_name`: The name of the product.
    - `product_url`: The URL of the product page.
    - `product_price`: The price of the product.
    - `image_url`: The URL of the product image.
    - `category_name`: The name of the category to which the product belongs.
    - `category_id`: The ID of the category to which the product belongs. This is a foreign key that references the `id` field 		  in the `categories_tb` table.

## Playwright

This project uses Playwright in the Scrapy settings. Playwright is a Node.js library to automate Chromium, Firefox, and WebKit browsers with a single API. It enables cross-browser web automation that is ever-green, capable, reliable, and fast. In this project, Playwright is used as a download handler for both HTTP and HTTPS URL schemes as product price are loaded lately in our scraping website.

## Scrapy-User-Agents

Scrapy-User-Agents is a middleware for Scrapy that provides a user-agent rotation based on the settings in settings.py, spider, request. A default User-Agent file is included in this repository, which contains about 2200 user agent strings. You can supply your own User-Agent file by setting RANDOM_UA_FILE.

## GitHub Actions Workflow

This repository uses a GitHub Actions workflow to run a web scraper every 2 hours. Here's a brief explanation of what each part does:

- `name: Run scraper`: This is the name of the workflow.
- `on: schedule: - cron: '0 */2 * * *'`: This sets the workflow to run on a schedule, specifically every 2 hours.
- `on: workflow_dispatch:`: This allows you to manually trigger the workflow from GitHub's UI.
- `jobs: build:`: This starts the definition of a job called `build`.
- `runs-on: ubuntu-latest`: This sets the job to run on the latest version of Ubuntu.
- `steps:`: This begins the list of steps that the job will run.
- `- uses: actions/checkout@v2`: This step checks out your repository so the workflow can access it.
- `- name: Set up Python`: This step sets up Python using the `actions/setup-python@v2` action.
- `- name: Install dependencies`: This step installs the dependencies listed in your `requirements.txt` file.
- `- name: Install Playwright browsers`: This step installs the browsers required by Playwright.
- `- name: Run scraper`: This step runs the `sastodeal_spider` scraper.
- `- name: Setup Git`: This step sets up Git with the email and username of "GitHub Action".
- `- name: Push changes`: This step commits any changes made during the run of the workflow and pushes them to the repository.

## Contributing

Contributions to this project are welcome. Please open an issue to discuss your proposed changes before making a pull request.
