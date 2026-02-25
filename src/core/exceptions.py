class APINotStartupError(Exception):
    pass


class ServersFullError(Exception):
    pass


class ServerCookieExpiredError(Exception):
    pass


class ServerReloginFailedError(Exception):
    pass


class NotFoundError(Exception):
    pass
