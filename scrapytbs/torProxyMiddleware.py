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
        password = get_project_settings()['TBS_TOR_PASSWORD']

        identity_renewal_rate = get_project_settings(
        )['TBS_IDENTITY_RENEWAL_RATE']
        req = identity_renewal_rate

        per_error_renewal = get_project_settings(
        )['TBS_PER_ERROR_RENEWAL']

        if req > 0:
            req -= 1
        else:
            new_tor_identity(password)
            req = identity_renewal_rate
            print('new tor identity')
            return request
        if response.status != 200 and per_error_renewal:
            new_tor_identity(password)
            print('new tor identity')
            return request
        return response

    def process_request(self, request, spider):
        # Set the Proxy
        # A new identity for each request
        # if TBS_PER_REQUEST_RENEWAL set to True
        password = get_project_settings()['TBS_TOR_PASSWORD']

        per_request_renewal = get_project_settings(
        )['TBS_PER_REQUEST_RENEWAL']

        if per_request_renewal:
            new_tor_identity(password)
        request.meta['proxy'] = 'http://127.0.0.1:8118'
