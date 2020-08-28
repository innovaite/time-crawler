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
        # Find the URLs on the current page:
        for url in response.css("h3.headline a::attr(href)"):
            yield response.follow(url, callback=self.parse_story)
            
        # Move to the next page:
        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page is not None and int(next_page.split("=")[1]) <= 200:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_story(self, response):
        # Find the drop cap if it exists:
        drop_cap = response.css("span.dropcap::text").get()
        drop_cap = "" if drop_cap is None else drop_cap

        # Concatenate the different elements of the body of the article:
        body = response.css("div.padded").css("p::text, p a::text, p em::text, p i::text, p a em::text, p a i::text").getall()
        body = "\n".join(body).split()
        body = drop_cap + " ".join(body)
        
        yield {
            "url": response.request.url,
            "title": "".join(response.css("h1.headline").css("::text").getall()).strip(),
            "author": response.css("a.author-name::text").get().strip(),
            "date": response.css("div.timestamp::text").get().strip(),
            "body": body
        }