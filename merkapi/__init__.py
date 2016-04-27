import certifi
import logging
import urllib3

from . import utils

log = logging.getLogger(__name__)

COUNTRY_CZ = 'cz'
COUNTRY_SK = 'sk'
COUNTRY_ALLOWED = (COUNTRY_CZ, COUNTRY_SK)


class Api(object):
    token = None

    def __init__(self, token, content_type='application/msgpack'):

        headers = urllib3.make_headers(keep_alive=True, accept_encoding=True, user_agent='merk-api-py')
        headers.update({
            'authorization': 'Token %s' % token,
            'accept': content_type,
            'content-type': content_type
        })
        self.loads = getattr(utils, 'loads_%s' % content_type.split('/')[1])
        self.http = urllib3.HTTPSConnectionPool(
            "api.merk.cz", cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), headers=headers,
            timeout=urllib3.Timeout(total=5), retries=urllib3.Retry(total=3))

    @property
    def subscriptions(self):
        r = self.http.request('GET', '/subscriptions/')
        return self.loads(r.data)

    def suggest_by_regno(self, regno, country_code=COUNTRY_CZ):
        if country_code not in COUNTRY_ALLOWED:
            raise RuntimeError("Country code %s is not allowed." % country_code)

        r = self.http.request('GET', '/suggest/',
                              fields={'regno': regno, 'country_code': country_code})

        if r.status == 204:
            return

        return self.loads(r.data)

    def suggest_by_email(self, email=None, country_code=COUNTRY_CZ):
        if country_code not in COUNTRY_ALLOWED:
            raise RuntimeError("Country code %s is not allowed." % country_code)

        r = self.http.request('GET', '/suggest/',
                              fields={'email': email, 'country_code': country_code})

        if r.status == 204:
            return

        return self.loads(r.data)
