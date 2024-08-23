import rpyc


class RpcError(EOFError, rpyc.core.vinegar.GenericException):
    def __init__(self, code: int = 1, error: str = ""):
        super().__init__(error)
        self.error = error
        self.code = code

    def __str__(self):
        if self.error:
            return self.code, self.error
        return self.code, "RPC调用服务[Auth-Service]出错"

