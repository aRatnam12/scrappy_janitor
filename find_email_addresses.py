# -*- coding: utf-8 -*-
import sys
import urllib2
from scrapy.crawler import CrawlerProcess
from scrappy_janitor.spiders.email_spider import EmailSpider


def main():
    """
    This is the main function that takes a url from stdin and starts the
    EmailSpider using CrawlerProcess.
    """
    input_url = sys.argv[1] if len(sys.argv) > 1 else ''
    try:
        check_url = urllib2.urlopen('http://' + input_url).geturl()
    except urllib2.URLError:
        print 'That is not a valid url, please check for any typos and try again.'
        while True:
            try:
                input_url = raw_input('Please input a valid url (i.e. \'google.com\') to scrape: ')
                check_url = urllib2.urlopen('http://' + input_url).geturl()
                break
            except urllib2.URLError:
                print 'That is not a valid url, please check for any typos and try again.'
            except NameError:
                print 'Please make sure you surround the inputted website in quotes!'

    max_page_crawls = raw_input('What is the max number of webpages that will be scraped? Press \'enter\' to default to 50. ')
    if len(max_page_crawls) and '1' <= max_page_crawls <= '500':
        max_page_crawls = int(max_page_crawls)
    else:
        max_page_crawls = 50

    # Remove the http://, https://, www. if they are there to ensure consistency
    start_url = check_url.split('//')[-1]
    start_url = start_url.split('www.')[-1]
    start_url = start_url.split('/')[0]

    ITEM_PIPELINES = {
        # Sets the pipeline to be used for EmailSpider, the number is used for order of pipelines
        'scrappy_janitor.pipelines.EmailPipeline': 300,
    }

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_ENABLED': False, # I chose to remove the log statements for clarity
        'ITEM_PIPELINES': ITEM_PIPELINES,
    })

    process.crawl(EmailSpider, start_url, max_page_crawls)
    process.start() # the script will block here until the crawling is finished

if __name__ == "__main__":
    main()