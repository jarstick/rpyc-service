from rpyc import connect, async_
from sanic import Sanic
from sanic.response import json
import json as Json


app = Sanic("sanic-authRpc")


@app.route("/user/login", methods=["POST"])
async def login(request):
    try:
        authConn = connect("localhost", 18861)
        asyncResult = async_(authConn.root.login)(**request.json)
        Result = asyncResult.value
        authConn.close()
        return json({"code": 0, "data": {"userInfo": Json.loads(Result)}, "msg": "success"})
    except Exception as e:
        return json({"code": 1, "data": None, "error": e.error})


@app.route("/user/register", methods=["POST"])
async def register(request):
    try:
        authConn = connect("localhost", 18861)
        asyncResult = async_(authConn.root.register)(**request.json)
        Result = asyncResult.value
        return json({"code": 0, "data": {"userInfo": Json.loads(Result)}, "msg": "success"})
    except Exception as e:
        return json({"code": 1, "data": None, "error": e.error})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
