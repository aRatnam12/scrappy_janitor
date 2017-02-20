# Welcome to Scrappy_Janitor!
For this project, I used the scrapy library to scrape the emails off a specified
webpage and print them to stdout. I scaffolded the project using scrapy's
included cli command, which is the reason for the slightly strange project structure.

The important files are:

1. `./scrappy_janitor/spiders/email_spider.py` This file is where the main scraper is. It extracts links from a page, follows these links based on allowed domains, and then extracts emails from each link's body and sends those to the EmailPipeline
2. `./scrappy_janitor/items.py` This file contains the EmailItem class which uses an Email field. Items in scrapy are used to send data from the spider to the Pipeline.
3. `./scrappy_janitor/pipelines.py` This file contains the EmailPipeline class which accepts EmailItems from EmailSpider to further process each email. The main usecase here is to maintain a set of emails to ensure that there are no duplicates being printed. The actual printing also happens in this file in the process_item function.


***Sidenote: scaffolding with the cli allows you to call the web scraper using scrapy's own
syntax which would look like `scrapy crawl email_spider -a website.com`, but I added in a
main run file (`./scrappy_janitor/find_email_addresses.py`)
to make it simpler for someone who is not familiar with scrapy.

## Setup
I setup a virtualenv so use that for best results!
You can run:

1. `virtualenv env`
2. `source env/bin/activate`
3. `pip install -r requirements.txt`

## Usage
You can extract emails from a page by running:
```
python find_email_addresses.py website.com
```

## Known shortcomings
I opted to use a regular expression to extract emails from the page rather than
extracting from links specifically such as by selecting the `mailto` on the
`href` of a link. This means that the scraper may contain some false positives
when text has a similar structure to an email such as `ios-image@2x.png`, but
will extract all emails that are in the body of a webpage.