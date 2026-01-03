import re
from scrapy.spiders import SitemapSpider

from scrapper.items import ArticleItem


class VsdSitemapSpider(SitemapSpider):
    name = "vsd_sitemap"
    allowed_domains = ["vsd.fr"]

    sitemap_urls = ["https://www.vsd.fr/sitemap_index.xml"]

    sitemap_rules = [
        (r"post-sitemap(\d*)?\.xml", "parse"),  # Follow all post-sitemap files
        # (r".*", "parse_article"),  # Parse all article URLs
        (
            r"^https://vsd\.fr/\d+-[^/]+/?$",
            "parse_article",
        ),  # Parse article URLs that start with a number
    ]
    max_articles = 2500
    articles_scraped = 0

    def sitemap_filter(self, entries):
        # Filter out unwanted URLs and only keep article URLs that start with a number
        for entry in entries:
            loc = entry["loc"]
            if "post-sitemap" in loc or (
                re.match(r"^https://vsd\.fr/\d+-[^/]+/?$", loc)
            ):
                yield entry

    def parse_article(self, response):
        if self.articles_scraped > self.max_articles:
            return

        try:
            item = ArticleItem()

            item["url"] = response.css('meta[property="og:url"]::attr(content)').get()

            item["title"] = response.css(
                'meta[property="og:title"]::attr(content)'
            ).get()

            item["author"] = response.css('meta[name="author"]::attr(content)').get()

            item["published_at"] = response.css(
                'meta[property="article:published_time"]::attr(content)'
            ).get()

            item["content"] = "\n\n".join(
                response.css("#post-content p::text").getall()
            )

            item["description"] = response.css(
                'meta[property="og:description"]::attr(content)'
            ).get()

            item["site_name"] = "vsd"

            self.articles_scraped += 1
            yield item
        except Exception as e:
            self.logger.error(f"Error processing {response.url}: {e}")
