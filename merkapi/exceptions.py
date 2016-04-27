class Unauthorized(Exception):
    pass


class Forbidden(Exception):
    pass


class BadRequest(Exception):
    pass


def by_status(code):
    if code in (200, 204):
        pass
    elif code == 400:
        raise BadRequest()
