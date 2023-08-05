from scrapy import Spider, Request
from scrapy.http import Response

from mayidaili import get_proxy_auth_header


class MayiProxyMiddleware:

    def process_request(self, request: Request, spider: Spider):
        if 'no_proxy' in request.meta:
            return None

        request.meta['proxy'] = 'http://s1.proxy.mayidaili.com:8123'
        auth_header = get_proxy_auth_header()
        request.headers['Mayi-Authorization'] = auth_header
        return None

    def process_response(self, request: Request, response: Response, spider: Spider):
        if 'no_proxy' in request.meta:
            return response

        if response.status in (407, 429):
            spider.logger.error('Response status code is {}. Response text: {}. Requests headers: {}'.format(
                response.status, response.text, request.headers))
        return response
