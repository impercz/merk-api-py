import json
import logging
import os.path


TEST_TOKEN = 'abcdef123456789'


def load_fixture(*args):
    fix_dir = os.path.join(
        os.path.dirname(__file__),
        'fixtures'
    )
    with open(os.path.join(fix_dir, *args)) as fp:
        return fp.read()


def request_callback(request):

    auth_token = request.headers.get('authorization', '')[6:]
    if not auth_token == TEST_TOKEN:
        return 401, {}, '{"detail": "Bad token"}'

    ct = request.headers['accept'].split('/')[1]
    params = {}
    try:
        url, query = request.url.split('?')
        query = query.split("&")
        for kv in query:
            k, v = kv.split("=")
            params[k] = v
    except ValueError:
        url = request.url

    filename = list(url.strip('/').split('/'))
    if 'regno' in params:

        # test 400 bad request
        try:
            int(params['regno'])
        except ValueError:
            return 400, {}, '{"regno": "Invalid regno"}'

        filename.append('regno')
        filename.append(str(params['regno']))

    if request.method == 'POST' and 'mget' in filename:
        rnos = json.loads(request.body)['regnos']
        filename.extend(rnos)

    if 'country_code' in params:
        filename.append(str(params['country_code']))
    filename = '-'.join(map(str, filename)) + '.%s' % ct

    # resource not found
    try:
        body = load_fixture(filename)
    except IOError:
        logging.warning("test fixture file not found: %s, returning 204 No Data" % filename)
        return 204, None, ''

    return 200, {}, body
