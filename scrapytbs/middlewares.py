"""This module contains the ``tbsMiddleware`` scrapy middleware"""

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.support.wait import WebDriverWait

from .http import tbsRequest

from tbselenium import tbdriver
from tbselenium.tbdriver import TorBrowserDriver


class tbsAddon:
    def update_settings(self, settings):
        settings['DOWNLOADER_MIDDLEWARES']['stb.scrapytbs.scrapytbs.tbsMiddleware'] = 800


class tbsMiddleware:
    """Scrapy middleware handling the requests using tor-browser-selenium"""

    def __init__(
            self,
            driver_name,
            browser_executable_path,
            driver_arguments,
            headless
    ):
        driver_options = getattr(tbdriver, "Options")
        # TODO implement driver_arguments
        # for argument in driver_arguments:
        #    driver_options.add_argument(argument)

        self.driver = TorBrowserDriver(
            browser_executable_path,
            headless=headless
        )

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""
        driver_name = 'tor-browser'

        browser_executable_path = crawler.settings.get(
            'TBS_BROWSER_EXECUTABLE_PATH')

        driver_arguments = crawler.settings.get('TBS_DRIVER_ARGUMENTS')

        headless = crawler.settings.get('TBS_DRIVER_HEADLESS')

        middleware = cls(
            driver_name=driver_name,
            browser_executable_path=browser_executable_path,
            driver_arguments=driver_arguments,
            headless=headless
        )

        crawler.signals.connect(
            middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        """Process a request using the tor-browser-selenium driver if applicable"""

        if not isinstance(request, tbsRequest):
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
