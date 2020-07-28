import scrapy

class TimeSpider(scrapy.Spider):
    name = "time"
    start_urls = [
        "https://time.com/section/us",
        "https://time.com/section/tech",
        "https://time.com/section/world",
        "https://time.com/section/ideas",
        "https://time.com/section/health",
        "https://time.com/section/sports",
        "https://time.com/section/science",
        "https://time.com/section/history",
        "https://time.com/section/politics",
        "https://time.com/section/business",
        "https://time.com/section/newsfeed",
        "https://time.com/section/entertainment"
    ]

    def parse(self, response):
        for url in response.css("h3.headline a::attr(href)"):
            yield response.follow(url, callback=self.parse_story)
        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page is not None and int(next_page.split("=")[1]) <= 200:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_story(self, response):
        yield {
            "url": response.request.url,
            "title": "".join(response.css("h1.headline").css("::text").getall()).strip(),
            "author": response.css("a.author-name::text").get().strip(),
            "date": response.css("div.timestamp::text").get().strip(),
            "body": "".join(response.css("div.padded").css("p::text, p a::text, p em::text, p i::text, p a em::text, p a i::text, p span.dropcap::text").getall()).strip()
        }
