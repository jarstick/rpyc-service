from re import Match

from authRpc.exc.err import RpcError


def validateEmail(email: str) -> Match[str] | None:
    import re
    pattern = re.compile(r"")
    return pattern.match(email) is not None


def validatePhone(phone: str) -> bool:
    import re
    pattern = re.compile(r"^1[3-9]\d{9}$")
    return pattern.match(phone) is not None


def validatePassword(password: str) -> bool:
    import re
    pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
    return pattern.match(password) is not None


def validateUsername(username: str) -> bool:
    import re
    pattern = re.compile(r"^[a-zA-Z0-9_-]{4,16}$")
    return pattern.match(username) is not None


def validateRegister(phone: str, password: str, username: str, email: str) -> bool:
    if not validateEmail(email):
        raise RpcError(error="邮箱格式错误!")
    if not validatePhone(phone):
        raise RpcError(error="手机号码格式错误!")
    if not validatePassword(password):
        raise RpcError(error="密码长度至少8位")
    if not validateUsername(username):
        raise RpcError(error="用户名格式错误!")
