class PrometheusWebException(Exception):
    pass


class InvalidCredentialsException(PrometheusWebException):
    pass


class NoLoggedInException(PrometheusWebException):
    pass
