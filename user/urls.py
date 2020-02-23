from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^$',views.users),
    url(r'/check_username_api',views.check_username_api),#注册填写用户名
    url(r'/check_password_api', views.check_password_api),#注册填写密码
    url(r'/check_password1_api', views.check_password1_api),#注册二次密码
    url(r'/check_email_api', views.check_email_api),#注册填写邮箱
    url(r'^/(?P<username>[\w]{6,18})/check_code_api$',views.check_code_api),#邮箱验证
    url(r'/login_check_api', views.login_check_api),#校验已经登陆无需再登陆
    url(r'^/(?P<username>[\w]{6,18})$',views.users,name='user'),#用户
    url(r'^/(?P<username>[\w]{6,18})/avatar$',views.user_avatar,name='user_avatar'),#头像
]