import unittest

import requests_mock

from securenative.config.securenative_options import SecureNativeOptions
from securenative.utils.request_utils import RequestUtils


class RequestUtilsTest(unittest.TestCase):

    def test_proxy_headers_extraction_from_request_ipv4(self):
        options = SecureNativeOptions(proxy_headers=['CF-Connecting-IP'])

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "CF-Connecting-IP": "203.0.113.1"}

            client_ip = RequestUtils.get_client_ip_from_request(request, options)

            self.assertEqual("203.0.113.1", client_ip)

    def test_proxy_headers_extraction_from_request_ipv6(self):
        options = SecureNativeOptions(proxy_headers=['CF-Connecting-IP'])

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "CF-Connecting-IP": "6559:6335:f572:14c6:4198:dd09:ddea:04f4"}

            client_ip = RequestUtils.get_client_ip_from_request(request, options)

            self.assertEqual("6559:6335:f572:14c6:4198:dd09:ddea:04f4", client_ip)

    def test_proxy_headers_extraction_from_request_multiple_ips(self):
        options = SecureNativeOptions(proxy_headers=['CF-Connecting-IP'])

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "CF-Connecting-IP": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

            client_ip = RequestUtils.get_client_ip_from_request(request, options)

            self.assertEqual("141.246.115.116", client_ip)
