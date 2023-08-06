from unittest import TestCase

import arivo
import requests_mock

from api import Client


class ClientUnitTest(TestCase):
    def setUp(self) -> None:
        arivo.api_url = "http://test"
        self.client = Client()
        super().setUp()

    def test_camel_to_snake(self):
        with requests_mock.mock() as m:
            m.register_uri(requests_mock.ANY, requests_mock.ANY, json={})

            self.client.Payment.StripeAPIKey.read(id="1")
            self.client.Payment.stripe_api_key.read(id="1")
            self.client.Payment.StripeApiKey.read(id="1")
            self.client.Payment.Stripe_apiKey.read(id="1")

        history = m.request_history
        self.assertEqual(4, len(history))

        correct_url = "http://test/payment/stripe_api_key/1/"
        for request in history:
            self.assertEqual(correct_url, request.url)
