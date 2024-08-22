from rpyc import connect, async_
from sanic import Sanic
from sanic.response import json
import json as Json
from loguru import logger as log


app = Sanic("sanic-authRpc")

try:
    authConn = connect("localhost", 18861)
except ConnectionRefusedError:
    log.error("auth-service不可用")


@app.route("/user/login", methods=["POST"])
async def login(request):
    try:
        asyncResult = async_(authConn.root.login)(**request.json)
        Result = asyncResult.value
        return json({"code": 0, "data": {"userInfo": Json.loads(Result)}, "msg": "success"})
    except Exception as e:
        log.error(e)
        return json({"code": 1, "data": None, "error": f"账号: {request.json.get("phone", "")}登录失败."})


@app.route("/user/register", methods=["POST"])
async def register(request):
    try:
        asyncResult = async_(authConn.root.register)(**request.json)
        Result = asyncResult.value
        return json({"code": 0, "data": {"userInfo": Json.loads(Result)}, "msg": "success"})
    except Exception as e:
        log.error(e)
        return json({"code": 1, "data": None, "error": f"注册用户[{request.json.get("username", "")}]失败"})


@app.route("/user/refreshToken", methods=["POST"])
async def refreshToken(request):
    try:
        asyncResult = async_(authConn.root.refreshToken)(**request.json)
        Result = asyncResult.value
        return json({"code": 0, "data": Json.loads(Result), "msg": "success"})
    except Exception as e:
        log.error(e)
        return json({"code": 1, "data": None, "error": e.error})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
