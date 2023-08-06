import grpc
from grpc import RpcError


class LazoError(grpc.RpcError):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class LazoUnavailableError(LazoError):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        error_msg = 'LazoClient failed to connect to server.' \
                    ' StatusCode: {} Details: {}' \
            .format(self.error.code(), self.error.details())
        return error_msg


class LazoInvalidArgumentError(LazoError):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        error_msg = 'Arguments sent by the client are invalid.' \
                    ' StatusCode: {} Details: {}' \
            .format(self.error.code(), self.error.details())
        return error_msg


class LazoUnexpectedError(LazoError):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        error_msg = 'An unexpected error was returned by the server.' \
                    ' StatusCode: {} Details: {}' \
            .format(self.error.code(), self.error.details())
        return error_msg


def lazo_client_exception(func):
    def _lazo_client_exception(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                raise LazoUnavailableError(e)
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise LazoInvalidArgumentError(e)
            else:
                raise LazoUnexpectedError(e)
    return _lazo_client_exception
