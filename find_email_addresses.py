# -*- coding: utf-8 -*-
import sys
from scrapy.crawler import CrawlerProcess
from scrappy_janitor.spiders.email_spider import EmailSpider


def main():
    """
    This is the main function that takes a url from stdin and starts the
    EmailSpider using CrawlerProcess.
    """
    input_url = sys.argv[1]
    start_url = input_url.split('www.')[-1] # Remove the www. if it's there to ensure consistency

    ITEM_PIPELINES = {
        # Sets the pipeline to be used for EmailSpider, the number is used for order of pipelines
        'scrappy_janitor.pipelines.EmailPipeline': 300,
    }

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_ENABLED': False, # I chose to remove the log statements for clarity
        'ITEM_PIPELINES': ITEM_PIPELINES,
    })

    process.crawl(EmailSpider, start_url)
    process.start() # the script will block here until the crawling is finished

if __name__ == "__main__":
    main()