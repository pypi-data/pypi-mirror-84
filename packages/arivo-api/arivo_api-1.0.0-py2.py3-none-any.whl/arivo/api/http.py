from urllib.parse import urljoin, urlencode

import arivo
import requests


class HttpBackend:
    def __init__(self, timeout):
        self._session = requests.Session()
        self.timeout = timeout

    def get_url(self, *args, **query_params):
        url = urljoin(arivo.api_url, "/".join(x.strip("/") for x in args)) + "/"
        if query_params:
            return f"{url}?{urlencode(query_params)}"
        else:
            return url

    def request(self, method, url_parts, body=None, query_params=None):
        query_params = query_params or {}
        url_parts = self.get_url(*url_parts, **query_params)
        if arivo.api_token:
            self._session.headers["Authorization"] = f"APIToken {arivo.api_token}"
        response = self._session.request(method, url_parts, json=body, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
