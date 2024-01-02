from urllib.parse import ParseResult, urlparse
from .parser import BookmarkRoot
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import scrapy
import os, re



class BookmarkSpider(Spider):
  name = "bookmark-spider"
  start_urls: list[str]
  allowed_domains: list[str]
  urls_visited: set[str]
  def __init__(self, start_url: str, output_path: str, *args, **kwargs):
    super(BookmarkSpider, self).__init__(*args, **kwargs)
    
    parsed_url = urlparse(start_url)
    self._domain = parsed_url.netloc.removeprefix("www.")
    
    self.start_urls = [start_url]
    self.allowed_domains = [self._domain]
    self._output_path = output_path
    

  def parse(self, response: HtmlResponse):
    print(f"Response received for {response.url}")
    url: ParseResult = urlparse(response.url)
    path: str = str(url.path).removesuffix("/") #paranoia
    tail: str | None = None
    filename = "index.html"
    if (slash_index:=path.rfind("/")) != -1:
      tail = path[slash_index+1:]
      if tail.find(".") != -1:
        filename = tail
        path = path[:slash_index]
    
    full_path = os.path.join(self._output_path, self._domain, path)
    print(f"Created directory: {full_path}")
    os.makedirs(full_path, exist_ok=True)
    
    with open(os.path.join(full_path, filename), mode='w') as f:
      f.write(response.text)
    
    
    
    
    
    follow_urls = response.xpath("(//a)/@href").getall()
    print(f"URLs found: {follow_urls}")
    
    return response.follow_all(
      follow_urls
    )
    
    
    
    # return response.follow(, self.parse_item)
    
        




# class BookmarkSpider(CrawlSpider):
#     name = "example.com"
#     allowed_domains = ["example.com"]
#     start_urls = ["http://www.example.com"]

#     rules = (
#         # Extract links matching 'category.php' (but not matching 'subsection.php')
#         # and follow links from them (since no callback means follow=True by default).
#         # Extract links matching 'item.php' and parse them with the spider's method parse_item
#         Rule(LinkExtractor(allow=(r".*",)), callback="parse_item"),
#     )

#     def parse_item(self, response):
#         self.logger.info("Hi, this is an item page! %s", response.url)
#         item = scrapy.Item()
#         item["id"] = response.xpath('//td[@id="item_id"]/text()').re(r"ID: (\d+)")
#         item["name"] = response.xpath('//td[@id="item_name"]/text()').get()
#         item["description"] = response.xpath(
#             '//td[@id="item_description"]/text()'
#         ).get()
#         item["link_text"] = response.meta["link_text"]
#         url = response.xpath('//td[@id="additional_data"]/@href').get()
#         return response.follow(
#             url, self.parse_additional_page, cb_kwargs=dict(item=item)
#         )

#     def parse_additional_page(self, response, item):
#         item["additional_data"] = response.xpath(
#             '//p[@id="additional_data"]/text()'
#         ).get()
#         return item


