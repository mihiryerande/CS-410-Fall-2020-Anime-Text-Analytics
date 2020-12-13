import re
import scrapy

"""
NOTE:
    Use this command:
        scrapy runspider animespider.py -O scraped.jl
"""


def clean_desc(desc):
    """
    Helper function to clean a given description, in case of any irregularity.

    Args:
        desc (str): A (mostly) clean bit of text to be cleaned up

    Returns:
        desc_clean (str): The cleaned-up input text
    """
    # Author note at end of desc
    desc = re.sub(r'\[.*(writ|sourc).*]', '', desc, flags=re.IGNORECASE)
    desc = re.sub(r'\(.*(writ|sourc).*\)', '', desc, flags=re.IGNORECASE)

    desc = ' '.join(desc.split())
    return desc


class AnimeSpider(scrapy.Spider):
    name = 'myanimelist'
    start_urls = [
        'https://myanimelist.net/topanime.php?type=tv'
    ]
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'CONCURRENT_REQUESTS':  10,
        'DOWNLOAD_DELAY':       2.5,
        'LOG_FILE':             'spider_log.txt',
        'RETRY_HTTP_CODES':     [500, 502, 503, 504, 522, 524, 408, 429, 403],  # Added 403 in case of traffic
        'ROBOTSTXT_OBEY':       True,
        'USER_AGENT':           'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/87.0.4280.66 Safari/537.36',

        # Uncomment for debugging
        # 'HTTPCACHE_ENABLED': True
    }

    empty_desc_strs = [
        'no synopsis has been added for this series yet',
        'no synopsis information has been added to this title'
    ]

    def parse_top_anime_page(self, response):
        """
        Spawn new requests from this page, and continue if necessary.

        Args:
            response: an HtmlResponse of the myanimelist page

        Returns:
            Dict(s) to be exported as a JSON with necessary data
        """
        for tr in response.css('tr.ranking-list'):
            # Found a valid anime to add to our collection
            href = tr.css('div[class="di-ib clearfix"] > h3 > a::attr(href)').get()
            yield scrapy.Request(response.urljoin(href), self.parse)

        # Possibly add next 'top-anime' page
        href = response.css('a[class="link-blue-box next"]::attr(href)').get()
        yield scrapy.Request(response.urljoin(href), self.parse)

        return None

    def parse_simple_page(self, response):
        """
        Parse a 'simple' page for a single Anime

        Args:
            response: an HtmlResponse of the myanimelist page

        Returns:
            Dict to be exported as a JSON with necessary data
        """
        # URL
        result = {'url': response.url}

        # Title
        title_raw = response.css('div[itemprop="name"] > h1 > strong::text').get()
        result['title'] = title_raw

        # Description
        desc_raw = response.xpath('string(.//p[@itemprop="description"])').get()
        desc_check = desc_raw.lower()
        for empty_desc_str in self.empty_desc_strs:
            if empty_desc_str in desc_check.lower():
                return None  # Exclude any anime without a real description

        desc_clean = clean_desc(desc_raw)
        result['description'] = desc_clean

        # Genres (as given by myanimelist)
        genres_raw = response.css('span[itemprop="genre"]::text').getall()
        genres_str = ','.join(genres_raw)
        result['mal genres'] = genres_str

        yield result
        return None

    def parse(self, response, **kwargs):
        """
        Two options:
            If the given page is a "top-anime" page, then create new requests and continue.
            Else, parse the given myanimelist page for the url/title/desc.

        Args:
            response: an HtmlResponse of the myanimelist page
            **kwargs: nothing, just included to match signature

        Returns:
            Dict(s) to be exported as a JSON with necessary data
        """
        if 'topanime.php' in response.url:
            result = self.parse_top_anime_page(response)
        else:
            result = self.parse_simple_page(response)
        return result
