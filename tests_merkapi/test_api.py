import merkapi
from unittest import TestCase
from urllib3_mock import Responses

from tests_merkapi.utils import request_callback, TEST_TOKEN

responses = Responses()

TEST_REGNO = 28547888


class JsonApiTests(TestCase):

    def setUp(self):
        responses.add_callback('GET', '/subscriptions/', callback=request_callback)
        responses.add_callback('GET', '/suggest/', callback=request_callback)
        responses.add_callback('GET', '/company/', callback=request_callback)
        responses.add_callback('POST', '/company/mget/', callback=request_callback)
        self.api = merkapi.Api(token=TEST_TOKEN, content_type='application/json')

    @responses.activate
    def test_subscriptions(self):
        r = self.api.subscriptions
        s = r.encdata

        assert len(s) == 2
        cz = s['cz']
        assert cz['api_enabled']
        assert not cz['api_throttled']

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == '/subscriptions/'

    @responses.activate
    def test_suggest_by_regno_pass(self):
        r = self.api.suggest(TEST_REGNO)
        assert len(r.encdata) == 1

        ret = r.encdata[0]
        assert ret['name'] == 'Imper CZ s.r.o.'
        assert ret['regno'] == TEST_REGNO

        assert len(responses.calls) == 1

    @responses.activate
    def test_suggest_by_email_pass(self):
        r = self.api.suggest('obchod@imper.cz', by='email')

        assert len(responses.calls) == 1

    @responses.activate
    def test_suggest_not_found(self):
        r = self.api.suggest(123456)
        assert r.status == 204

    @responses.activate
    def test_suggest_400(self):
        r = self.api.suggest('asd')
        assert r.status == 400
        assert 'regno' in r.encdata

    @responses.activate
    def test_company(self):
        r = self.api.company(TEST_REGNO)
        assert r.status == 200
        ret = r.encdata[0]
        assert len(ret['body']['persons']) == 2
        assert len(responses.calls) == 1

    @responses.activate
    def test_company_not_found(self):
        r = self.api.company(123456)
        assert r.status == 204

    @responses.activate
    def test_company_mget(self):
        r = self.api.companies([TEST_REGNO, 12345])
        assert r.status == 200
        ret = r.encdata
        assert len(ret) == 1

        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == 'POST'
