import json
import hashlib
import time
import jwt
from django.http import JsonResponse
# Create your views here.
from user.models import UserProfiles


# 校验登陆
def stoken(request):
    # 校验请求方式是否为POST
    if not request.method == 'POST':
        result = {"code": 501, "error": "请使用POST方式提交"}
        return JsonResponse(result)
    # 校验用户名是否为空
    json_bytes = request.body
    json_obj = json.loads(json_bytes)
    username = json_obj.get('username')
    if not username:
        result = {"code": 502, "error": "用户名不能为空"}
        return JsonResponse(result)
    # 校验用户名是否存在
    users = UserProfiles.objects.filter(username=username)
    if not users:
        result = {"code": 503, "error": "用户名不存在"}
        return JsonResponse(result)
    # 校验密码
    password = json_obj.get('password')
    h_p = hashlib.sha1()
    h_p.update(password.encode())
    pwd = h_p.hexdigest()
    pwd1 = users[0].password
    if pwd1 != pwd:
        result = {"code": 504, "error": "用户名或密码错误"}
        return JsonResponse(result)
    # 校验通过
    token = make_token(username)
    result = {"code": 500, "username": username, "data": {"token": token.decode()}}
    return JsonResponse(result)


def make_token(username, expire=3600 * 24):
    """
    生成token
    @param username:
    @param expire:
    @return:
    """
    key = 'abcd1234'
    now = time.time()
    payload = {"username": username, "exp": int(now) + expire}
    return jwt.encode(payload, key, algorithm="HS256")
