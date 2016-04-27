import merkapi
from unittest import TestCase
from urllib3_mock import Responses

from tests_merkapi.utils import request_callback, TEST_TOKEN

responses = Responses()
responses.add_callback('GET', '/subscriptions/', callback=request_callback, content_type='application/msgpack')
responses.add_callback('GET', '/suggest/', callback=request_callback, content_type='application/msgpack')


def test_unauth():
    api = merkapi.Api(token='nonono')
    assert api.subscriptions


class JsonApiTests(TestCase):

    def setUp(self):
        self.api = merkapi.Api(token=TEST_TOKEN, content_type='application/json')

    @responses.activate
    def test_subscriptions(self):
        s = self.api.subscriptions

        assert s['cz']['api_enabled']
        assert not s['cz']['api_throttled']
