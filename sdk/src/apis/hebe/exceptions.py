class HebeClientException(Exception):
    pass


class NotFoundEndpointException(HebeClientException):
    pass


class NoUnitSymbolException(HebeClientException):
    pass


class NoPermissionsException(HebeClientException):
    pass


class InvalidRequestEnvelopeStructure(HebeClientException):
    pass


class InvalidRequestHeadersStructure(HebeClientException):
    pass


class UnauthorizedCertificateException(HebeClientException):
    pass


class NotFoundEntityException(HebeClientException):
    pass


class UsedTokenException(HebeClientException):
    pass


class InvalidPINException(HebeClientException):
    pass


class ExpiredTokenException(HebeClientException):
    pass
