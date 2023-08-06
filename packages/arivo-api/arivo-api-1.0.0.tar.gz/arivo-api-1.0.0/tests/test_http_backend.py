from unittest import TestCase

import arivo
import requests_mock

from api import HttpBackend


class HttpBackendUnitTest(TestCase):
    def test_get_url(self):
        backend = HttpBackend(1)

        arivo.api_url = "http://test"
        self.assertTrue(backend.get_url("a", "b").startswith(arivo.api_url))

        # always ends with a slash
        self.assertTrue(backend.get_url("a", "b").endswith("/"))

        # slashes in parts are ignored
        self.assertEqual(backend.get_url("/a", "/b/", "c/"), "http://test/a/b/c/")

    def test_authorization_header_is_not_set(self):
        backend = HttpBackend(1)
        with requests_mock.mock() as m:
            m.register_uri(requests_mock.ANY, requests_mock.ANY, json={})

            arivo.api_token = None
            backend.request("get", ["test"])
            arivo.api_token = ""
            backend.request("get", ["test"])

        history = m.request_history
        self.assertEqual(2, len(history))

        req1, req2 = history
        self.assertNotIn("Authorization", req1.headers)
        self.assertNotIn("Authorization", req2.headers)

    def test_authorization_header_is_set(self):
        backend = HttpBackend(1)
        with requests_mock.mock() as m:
            m.register_uri(requests_mock.ANY, requests_mock.ANY, json={})

            arivo.api_token = "test123"
            backend.request("get", ["test"])

        history = m.request_history
        self.assertEqual(1, len(history))

        req = history[0]
        self.assertIn("Authorization", req.headers)
        self.assertEqual("APIToken test123", req.headers["Authorization"])
