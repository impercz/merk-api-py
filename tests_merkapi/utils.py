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
    print(request)

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
    method = request.method

    filename = url.strip('/').split('/')
    if 'regno' in params:
        filename.append(str(params['regno']))
    if 'country_code' in params:
        filename.append(str(params['country_code']))
    filename = '-'.join(filename) + '.%s' % ct
    body = load_fixture(filename)
    return 200, {}, body
