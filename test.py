import os
from bookmarklib.crawler import BookmarkSpider

from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings

from urllib.parse import urlparse


parsed_url = urlparse("http://www.example.com/hello/world.html")
path = parsed_url.path
print(parsed_url.netloc)


os.environ["SCRAPY_SETTINGS_MODULE"] = "bookmarklib.settings"


settings = get_project_settings()
print(settings.attributes)

# process = CrawlerProcess(settings)

# process.crawl(BookmarkSpider, start_url="https://www.wikipedia.org/", output_path="/home/shino/test/bookmarks")
# process.start()

