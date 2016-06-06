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
    _enums = {}

    def __init__(self, token, content_type='application/msgpack'):

        headers = urllib3.make_headers(keep_alive=True, accept_encoding=True, user_agent='merk-api-py')
        headers.update({
            'authorization': 'Token %s' % token,
            'accept': content_type,
            'content-type': content_type
        })
        self.loads = getattr(utils, 'loads_%s' % content_type.split('/')[1])
        self.dumps = getattr(utils, 'dumps_%s' % content_type.split('/')[1])
        self.http = urllib3.HTTPSConnectionPool(
            "api.merk.cz", cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), headers=headers,
            timeout=urllib3.Timeout(total=5), retries=urllib3.Retry(total=3))

    @property
    def subscriptions(self):
        """
        :return: Your subscription information for each country set (cz, sk)
        """

        r = self.http.request('GET', '/subscriptions/')
        r.encdata = self.loads(r.data) if r.data else None
        return r

    def suggest(self, query, by='regno', country_code=COUNTRY_CZ):
        """
        Suggest company info by regno, by email or by name

        :param query:
        :param by: one of: 'regno', 'email', 'name'
        :param country_code: one of 'cz', 'sk'
        :return:
        """

        r = self.http.request('GET', '/suggest/',
                              fields={by: query, 'country_code': country_code})

        r.encdata = self.loads(r.data) if r.data else None
        return r

    def company(self, regno, country_code=COUNTRY_CZ):
        """
        :param regno: Valid regno
        :param country_code: one of 'cz', 'sk'
        :return: Company info
        """

        r = self.http.request('GET', '/company/',
                              fields={'regno': regno, 'country_code': country_code})

        r.encdata = self.loads(r.data) if r.data else None
        return r

    def companies(self, regnos, country_code=COUNTRY_CZ):

        r = self.http.request('POST', '/company/mget/',
                              body=self.dumps({'regnos': regnos, 'country_code': country_code}))

        r.encdata = self.loads(r.data) if r.data else None
        return r

    def get_enums(self, country_code=COUNTRY_CZ):

        if self._enums.get(country_code, None):
            return self._enums[country_code]
        else:
            r = self.http.request('GET', '/enums/', fields={country_code: country_code})
            self._enums[country_code] = self.loads(r.data)
            return self._enums[country_code]
