import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from validate_email import validate_email
from ..items import EmailItem

class EmailSpider(CrawlSpider):
    """
    Main spider class. The crawler starts this spider. The process follows:
    1) The spider takes the start_url arg and instantiates the start domains
    2) The spider uses the LinkExtractor to get all links on the page.
    3) The LinkExtractor uses the process_links function to filter only
    the links that are in the same domain as start_url
    4) The callback parse_link is invoked for each filtered link
    5) Parse_link uses a regexp to find all emails on the page and generates
    an EmailItem for each valid email
    6) Each EmailItem is passed to the EmailPipeline for further processing
    such as ensuring there are no duplicates in our case
    """
    name = "email_spider"

    rules = (
        Rule(
            LinkExtractor(),
            callback='parse_link',
            follow=True,
            process_links='filter_links',
        ),
    )

    def __init__(self, start_url, *args, **kwargs):
        super(EmailSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = [start_url, 'www.' + start_url] # Only use the base domain to make sure subdomains are ignored
        self.start_urls = ['http://www.' + start_url] # start_urls needs the http

    def parse_link(self, response):
        """
        Invoked for each link that is followed by the spider.
        Finds all emails in the body of the page using a regexp.
        Validates the email using validate_email.
        Returns all validated emails as EmailItems to the EmailPipeline
        """
        emails = set(re.findall(r'[\w\.-]+@[\w-]+\.[\w]+', response.body))
        for email in emails:
            if validate_email(email):
                email_item = EmailItem()
                email_item['email'] = email
                yield email_item

    def filter_links(self, links):
        """
        Filters all links that are extracted by the LinkExtractor.
        Returns only the links that are in allowed domains.
        """
        def in_allowed_domains(link):
            cleaned_url = link.url.split('//')[-1] # Remove https:// or http://
            domain = cleaned_url.split('/')[0] # Remove any routes after the domain
            return (domain in self.allowed_domains)

        return filter(in_allowed_domains, links)

