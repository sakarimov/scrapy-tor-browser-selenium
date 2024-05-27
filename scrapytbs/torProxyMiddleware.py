from stem import Signal
from stem.control import Controller
from stem.util.log import get_logger
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.utils.project import get_project_settings

logger = get_logger()
logger.propagate = False


def new_tor_identity(password):
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=password)
        controller.signal(Signal.NEWNYM)


class torProxyMiddleware(HttpProxyMiddleware):
    def process_response(self, request, response, spider):
        # Get a new identity depending on the response
        password = get_project_settings('TBS_TOR_PASSWORD')
        if response.status != 200:
            new_tor_identity(password)
            return request
        return response

    def process_request(self, request, spider):
        # Set the Proxy
        # A new identity for each request
        # Comment out if you want to get a new Identity only through process_response
        password = get_project_settings('TBS_TOR_PASSWORD')
        new_tor_identity(password)
        request.meta['proxy'] = 'http://127.0.0.1:8118'
