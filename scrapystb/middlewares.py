"""This module contains the ``stbMiddleware`` scrapy middleware"""

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.support.wait import WebDriverWait

from .http import stbRequest

from tbselenium.tbdriver import TorBrowserDriver


class stbAddon:
    def update_settings(self, settings):
        settings['DOWNLOADER_MIDDLEWARES']['stb.scrapystb.scrapystb.stbMiddleware'] = 800


class stbMiddleware:
    """Scrapy middleware handling the requests using selenium"""

    def __init__(self, driver_name):

        self.driver = TorBrowserDriver(
            '/home/sulthan/.local/opt/tor-browser/app/')

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""
        driver_name = 'tor-browser'

        middleware = cls(
            driver_name=driver_name,
        )

        crawler.signals.connect(
            middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""

        if not isinstance(request, stbRequest):
            return None

        self.driver.get(request.url)

        if request.wait_until:
            WebDriverWait(self.driver, request.wait_time).until(
                request.wait_until
            )

        if request.screenshot:
            request.meta['screenshot'] = self.driver.get_screenshot_as_png()

        if request.script:
            self.driver.execute_script(request.script)

        body = str.encode(self.driver.page_source)

        request.meta.update({'driver': self.driver})

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""

        self.driver.quit()
