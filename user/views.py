import hashlib
import json
import re
import jwt
from django.http import JsonResponse
from stoken.views import make_token
from tool.login_check import login_check
from user.models import UserProfiles
import time
from django.core.mail import send_mail
from random import choice
from stocks_tools import settings


# 注册页面的clur事件
def check_username_api(request):
    # 校验请求是否为GET
    if not request.method == 'GET':
        result = {"code": 900, "error": "请使用GET方式提交"}
        return JsonResponse(result)
    # 校验请求是否为空
    username = request.GET.get('username')
    if not username:
        result = {"code": 901, "error": "用户名不能为空"}
        return JsonResponse(result)
    # 校验用户名字符是否合法
    re_username = re.findall("^[A-Za-z0-9-_]+$", username)
    if not re_username:
        result = {"code": 902, "error": "只能输入字母、数字、下划线"}
        return JsonResponse(result)
    # 校验用户名长度是否合法
    if not 6 <= len(username) <= 18:
        result = {"code": 903, "error": "长度应为6～18个字符"}
        return JsonResponse(result)
    # 校验用户名是否存在
    users = UserProfiles.objects.filter(username=username).first()
    if users:
        result = {"code": 904, "error": "该用户名已被注册"}
        return JsonResponse(result)
    result = {"code": 900, "error": "该用户名可用"}
    return JsonResponse(result)


# 密码校验
def check_password_api(request):
    # 校验请求是否为GET
    if not request.method == 'GET':
        result = {"code": 801, "error": "请使用GET方式提交"}
        return JsonResponse(result)
    # 校验密码是否为空
    password = request.GET.get('password')
    if not password:
        result = {"code": 802, "error": "密码不能为空"}
        return JsonResponse(result)
    # 校验密码字符是否合法
    re_password = re.findall("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).*$", password)
    if not re_password:
        result = {"code": 803, "error": "密码必须由大写、小写、数字组成"}
        return JsonResponse(result)
    # 校验密码长度是否合法
    if not 9 <= len(password) <= 16:
        result = {"code": 804, "error": "密码长度应为6～16个字符"}
        return JsonResponse(result)
    result = {"code": 800, "error": "密码可用"}
    return JsonResponse(result)


# 校验二次密码
def check_password1_api(request):
    password = request.GET.get('password')
    password1 = request.GET.get("password1")
    if password != password1:
        result = {"code": 805, "error": "二次输入密码不一致"}
        return JsonResponse(result)
    if not password1:
        result = {"code": 805, "error": "两次输入密码不能为空"}
        return JsonResponse(result)
    result = {"code": 806, "error": "密码一致"}
    return JsonResponse(result)


# 校验邮箱
def check_email_api(request):
    # 校验请求是否为GET
    if not request.method == 'GET':
        result = {"code": 701, "error": "请使用GET方式提交"}
        return JsonResponse(result)
    # 校验邮箱是否为空
    email = request.GET.get('email')
    if not email:
        result = {"code": 702, "error": "邮箱不能为空"}
        return JsonResponse(result)
    # 校验邮箱是否合法
    if not re.match(r'^([a-zA-Z\.0-9]+)@[a-zA-Z0-9]+\.[a-zA-Z]{3}$', email):
        result = {"code": 703, "error": "邮箱格式不正确"}
        return JsonResponse(result)
    if UserProfiles.objects.filter(email=email):
        result = {"code": 704, "error": "该邮箱已被注册，请更换邮箱"}
        return JsonResponse(result)
    result = {"code": 700, "error": "邮箱可用"}
    return JsonResponse(result)


# 用户注册
@login_check('PUT')
def users(request, username=None):
    if request.method == 'GET':
        # 检查请求是否包含用户名
        if username:
            # 如果包含用户名，校验是否存在
            try:
                user = UserProfiles.objects.get(username=username)
            except Exception:
                user = None
            if not user:
                result = {"code": 503, "error": "用户名不存在"}
                return JsonResponse(result)
            # 检查是否包含查询字符串
            if request.GET.keys():
                data = {}
                for key in request.GET.keys():
                    # 判断user是否包含key属性
                    if hasattr(user, key):
                        data[key] = getattr(user, key)
                result = {"code": 400, "username": username, "data": data}
                return JsonResponse(result)
            # 查询用户全量数据
            else:
                list_stock = user.showdata_set.all()
                list_code =[stock.code for stock in list_stock]
                data = {
                    "email": user.email,
                    "gender": user.gender,
                    "age": user.age,
                    "avatar": str(user.avatar),
                    "salary": user.salary,
                    "Occupation": user.Occupation,
                    "partiality": user.partiality,
                    "experience": user.experience,
                    "lever": user.lever,
                    "stock":list_code
                }
                result = {"code": 400, "username": username, "data": data}
                return JsonResponse(result)
        else:
            result = {"code": 404, "error": "您访问的页面有误或不存在"}
            return JsonResponse(result)
    elif request.method == 'POST':
        json_str = request.body
        if not json_str:
            result = {"code": 601, "error": "请求数据不能为空"}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        username = json_obj['username']
        password = json_obj['password']
        email = json_obj['email']
        # username校验
        if not username:
            result = {"code": 602, "error": "用户名不能为空"}
            return JsonResponse(result)
        users = UserProfiles.objects.filter(username=username)
        if users:
            result = {"code": 603, "error": "该用户名已被注册"}
            return JsonResponse(result)

        # 插入数据
        h_p = hashlib.sha1()
        h_p.update(password.encode())
        pwd = h_p.hexdigest()
        try:
            UserProfiles.objects.create(username=username, password=pwd, email=email)
        except Exception as e:
            print('UserProfiles create error is %s' % (e))
            result = {"code": 604, "error": "注册失败，该用户名可能已被注册，请重新注册"}
            return JsonResponse(result)
        # make token
        token = make_token(username)
        result = {"code": 600, "username": username, "data": {"token": token.decode()}}
        return JsonResponse(result)
    # 用户修改
    elif request.method == 'PUT':
        user = request.user
        # 校验json是否为空
        json_bytes = request.body
        if not json_bytes:
            result = {"code": 601, "error": "请求数据不能为空"}
            return JsonResponse(result)
        json_obj = json.loads(json_bytes)
        user.gender = json_obj.get('gender')
        user.age = json_obj.get('age')
        user.salary = json_obj.get('salary')
        user.Occupation = json_obj.get('Occupation')
        user.partiality = json_obj.get('partiality')
        user.experience = json_obj.get('experience')
        user.lever = json_obj.get('lever')
        user.save()
        result = {"code": 500, "username": username}
        return JsonResponse(result)
    result = {"code": 605, "error": "请求方式不正确"}
    return JsonResponse(result)


# 上传头像
@login_check('POST')
def user_avatar(request, username):
    # 校验请求方式是否为POST
    if not request.method == 'POST':
        result = {"code": 301, "error": "请求方式必须为POST"}
        return JsonResponse(result)
    users = UserProfiles.objects.filter(username=username)
    # 校验用户是否存在
    if not users:
        result = {"code": 503, "error": "该用户不存在"}
        return JsonResponse(result)
    # 校验头像是否存在
    if request.FILES.get('avatar'):
        users[0].avatar = request.FILES['avatar']
        users[0].save()
        result = {"code": 500, "username": username}
        return JsonResponse(result)
    else:
        result = {"code": 302, "error": "头像不能为空"}
        return JsonResponse(result)


def login_check_api(request):
    if request.method == 'GET':
        # 检查请求是否包含用户名
        username = request.GET.get('username')
        if username:
            # 如果包含用户名，校验是否存在
            try:
                user = UserProfiles.objects.get(username=username)
            except Exception:
                user = None
            if not user:
                result = {"code": 503, "error": "用户名不存在"}
                return JsonResponse(result)
    token = request.META.get('HTTP_AUTHORIZATION')
    try:
        res = jwt.decode(token, 'abcd1234', algorithms='HS256')
    except Exception as e:
        print('token error is %s' % e)
        result = {"code": 1002, "error": "请登陆"}
        return JsonResponse(result)
    username = res['username']
    user = UserProfiles.objects.get(username=username)
    email = user.email
    result = {"code": 1000, "username": username, "email": email}
    return JsonResponse(result)


# 获取settings中的验证码长度和有效期
code_length = settings.CODE_LENGTH
valid_time = settings.CODE_VALID_TIME


# 生成验证码/未来失效时间/生成时间
def make_email_code(code_length, valid_time):
    code_source = '1234567890'
    code = ''
    for i in range(code_length):
        code += choice(code_source)
    code_valid_time = int(time.time()) + valid_time
    make_time = time.strftime('%Y-%m-%d %H-%M-%S')
    return code, code_valid_time, make_time


# 验证码校验
@login_check('GET', 'POST', 'PUT')
def check_code_api(request, username):
    # GET 获取邮箱验证页面
    if request.method == 'GET':
        if not username:
            result = {"code": 602, "error": "用户名不能为空"}
            return JsonResponse(result)
        users = UserProfiles.objects.filter(username=username)
        if not users:
            result = {"code": 503, "error": "该用户不存在"}
            return JsonResponse(result)
        else:
            result = {"code": 1000, "username": users[0].username, "email": users[0].email}
            return JsonResponse(result)
    # POST 获取验证码
    elif request.method == 'POST':
        email_from = settings.EMAIL_FROM
        json_bytes = request.body
        json_obj = json.loads(json_bytes)
        user_email = json_obj.get('email')
        send_type = json_obj.get('send_type')
        # 校验验证类型码是否存在
        if not send_type:
            result = {"code": 1003, "error": "没有提交验证类型码"}
            return JsonResponse(result)
        # 校验是否提交用户名
        if not username:
            result = {"code": 602, "error": "用户名不能为空"}
            return JsonResponse(result)
        # 校验用户是否存在
        user = UserProfiles.objects.filter(username=username)
        if not user:
            result = {"code": 503, "error": "用户名不存在"}
            return JsonResponse(result)
        # 校验邮箱是否提交邮箱
        if not user_email:
            result = {"code": 1002, "error": "没有提交邮箱"}
            return JsonResponse(result)
        # 校验邮箱是否一致
        if user_email != user[0].email:
            result = {"code": 1004, "error": "用户邮箱不一致"}
            return JsonResponse(result)
        # 注册激活码验证/获取验证码/失效时间戳/生成时间
        code, code_valid_time, make_time = make_email_code(code_length, valid_time)
        # 插入数据
        user[0].check_code = code
        user[0].code_valid_time = code_valid_time
        user[0].save()
        # 校验验证类型码是否合法
        if send_type not in ['0', '1', '2']:
            result = {"code": 1001, "error": "验证类型码错误，必须是0/1/2之一"}
            return JsonResponse(result)
        # 根据不同send_type匹配不同邮件模板
        text = [('【STAT】账号注册“邮箱验证激活”',
                 '<p style="font-size:18px; font-family:微软雅黑">尊敬的<span style="color:#FF0000">' + username + '</span>您好!</p><p style="font-size:18px; font-family:微软雅黑">感谢您使用SDAT平台，您于<span style="color:#FF0000">' + make_time + '</span>正在进行账号注册邮箱验证操作</p><p style="font-size:18px; font-family:微软雅黑">本次验证码是：<span style="font-size:36px; font-weight:bold; color:#3366CC; font-family:微软雅黑">' + code + '</span></p><p style="font-size:18px; font-family:微软雅黑">验证码在30分钟内有效，30分钟后需重新激活!</p><p style="font-size:18px; font-family:微软雅黑">谢谢！<br>SDAT 团队</p>')
            , ('【STAT】密码修改“邮箱验证激活”',
               '<p style="font-size:18px; font-family:微软雅黑">尊敬的<span style="color:#FF0000">' + username + '</span>您好!</p><p style="font-size:18px; font-family:微软雅黑">感谢您使用SDAT平台，您于<span style="color:#FF0000">' + make_time + '</span>正在进行密码修改邮箱验证操作</p><p style="font-size:18px; font-family:微软雅黑">本次验证码是：<span style="font-size:36px; font-weight:bold; color:#3366CC; font-family:微软雅黑">' + code + '</span></p><p style="font-size:18px; font-family:微软雅黑">验证码在30分钟内有效，30分钟后需重新激活!</p><p style="font-size:18px; font-family:微软雅黑">谢谢！<br>SDAT 团队</p>')
            , ('【STAT】邮箱修改“邮箱验证激活”',
               '<p style="font-size:18px; font-family:微软雅黑">尊敬的<span style="color:#FF0000">' + username + '</span>您好!</p><p style="font-size:18px; font-family:微软雅黑">感谢您使用SDAT平台，您于<span style="color:#FF0000">' + make_time + '</span>正在进行邮箱修改邮箱验证操作</p><p style="font-size:18px; font-family:微软雅黑">本次验证码是：<span style="font-size:36px; font-weight:bold; color:#3366CC; font-family:微软雅黑">' + code + '</span></p><p style="font-size:18px; font-family:微软雅黑">验证码在30分钟内有效，30分钟后需重新激活!</p><p style="font-size:18px; font-family:微软雅黑">谢谢！<br>SDAT 团队</p>')]
        # 根据验证类型码匹配邮件模板
        title = text[int(send_type)][0]  # /text_templates/email_check_text.py
        body = text[int(send_type)][1]  # /text_templates/email_check_text.py
        send_mail(title, '', email_from, [user_email], html_message=body)
        result = {"code": 1005, "email": user[0].email, "error": "验证码发送成功"}
        return JsonResponse(result)

    # PUT 验证码校验
    elif request.method == 'PUT':
        if not username:
            result = {"code": 602, "error": "用户名不能为空"}
            return JsonResponse(result)
        # 校验用户是否存在
        users = UserProfiles.objects.filter(username=username)
        if not users:
            result = {"code": 503, "error": "用户名不存在"}
            return JsonResponse(result)
        json_str = request.body
        # 校验请求数据是否为空
        if not json_str:
            result = {"code": 601, "error": "请求数据不能为空"}
            return JsonResponse(result)
        json_dict = json.loads(json_str)
        check_code = json_dict['check_code']
        # 校验验证码是否为空
        if not check_code:
            result = {"code": 1006, "error": "验证码不能为空"}
            return JsonResponse(result)
        # 校验验证码是否匹配
        if int(check_code) != users[0].check_code:
            result = {"code": 1007, "error": "验证码错误"}
            return JsonResponse(result)
        # 校验验证码是否过期
        if users[0].code_valid_time < time.time():
            result = {"code": 1008, "error": "验证码已过期"}
            return JsonResponse(result)
        # 否则验证成功
        result = {"code": 1009, "error": "验证成功"}
        return JsonResponse(result)
