from re import Match


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

