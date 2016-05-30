import sys
import json
import logging
import msgpack
from msgpack.exceptions import UnpackValueError

log = logging.getLogger(__name__)

PY_VERSION = sys.version_info[0]


def loads_msgpack(data):
    try:
        return msgpack.loads(data, encoding='utf-8')
    except UnpackValueError as e:
        log.error('Cannot unpack response from Merk API: %s' % e)


def loads_json(data):
    data = data.decode('utf-8') if PY_VERSION == 3 else data
    try:
        return json.loads(data, encoding='utf-8')
    except ValueError as e:
        log.error('Cannot unpack response from Merk API: %s' % e)


def dumps_json(data):
    return json.dumps(data, ensure_ascii=False)


def dumps_msgpack(data):
    return msgpack.dumps(data)
