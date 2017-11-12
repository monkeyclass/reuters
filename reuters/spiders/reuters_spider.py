from scrapy import Spider
from scrapy import Request
#from scrapy.selector import Selector
from urllib.parse import urljoin
from reuters.items import ReutersItem
#from scrapy.contrib.linkextractors import LinkExtractor
#from scrapy.contrib.spiders import CrawlSpider, Rule


class ReutersSpider(Spider):
    name = "reuters"
    allowed_domains = ["reuters.com"]
	# Currently set to scrape the financial news section. Can be changed by changing the 'bank' in the link.
	# Should probably add a loop before the current that goes through multiple sections.
    def start_requests(self):
		# The range is from 1 - 3277 pages. The current maximum for most sections. Change as to the max number of pages.
		# Also possible to specify a lower number, if more interested in latest news. 
		# The pipeline to MongoDB ensures there will be no duplicate documents
        for i in range(1, 3277):
            page = 'http://www.reuters.com/news/archive/banks?view=page&page='+str(i)+'&pageSize=10'
            yield Request(url=page, callback=self.parse)

    def parse(self, response):
        links = response.xpath('//div[@class="story-content"]/a/@href').extract()
        for l in links:
            url = urljoin('http://www.reuters.com', l)
            yield Request(url, callback=self.parse_article)

    def parse_article(self, section):
            Item = ReutersItem()
            Item['timestamp'] = section.xpath('//div[@class="ArticleHeader_date_V9eGk"]/text()').extract_first()
            Item['headline'] = section.xpath('//h1[@class="ArticleHeader_headline_2zdFM"]/text()').extract_first()
            Item['text'] = "\n".join(section.xpath('//div[@class="ArticleBody_body_2ECha"]/p/text()').extract())
            yield Item
