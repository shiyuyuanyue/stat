import jwt
from django.http import JsonResponse
from user.models import UserProfiles

KEY = 'abcd1234'


def login_check(*methods):
    def _login_check(func):
        def wrapper(request, *args, **kwargs):
            token = request.META.get('HTTP_AUTHORIZATION')
            # 校验使用装饰其是否传参method
            if not methods:
                return func(request, *args, **kwargs)
            # 校验method是否需要校验
            if not request.method in methods:
                return func(request, *args, **kwargs)
            # 校验是否获取到了token
            if not token:
                result = {"code": 101, "error": "没有获取到token"}
                return JsonResponse(result)
            # 解密与校验token是否合法
            try:
                res = jwt.decode(token, KEY, algorithms='HS256')
            except Exception as e:
                print('token error is %s' % e)
                result = {"code": 102, "error": "请登陆"}
                return JsonResponse(result)
            username = res['username']
            user = UserProfiles.objects.get(username=username)
            request.user = user
            return func(request, *args, **kwargs)

        return wrapper

    return _login_check
