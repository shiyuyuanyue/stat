from django.db import models


# Create your models here.
class UserProfiles(models.Model):
    username = models.CharField(max_length=30, primary_key=True, verbose_name='用户名')
    password = models.CharField(max_length=160, verbose_name='密码')
    email = models.EmailField(max_length=60, verbose_name='邮箱')
    gender = models.CharField(max_length=4, verbose_name='性别', null=True, default='未填写')
    age = models.CharField(max_length=4, verbose_name='年龄', null=True, default='未填写')
    avatar = models.ImageField(max_length=1000, upload_to='statoc/avatar/%Y/%m/%d/', verbose_name='头像', null=True)
    salary = models.CharField(max_length=6, verbose_name='工资', null=True, default='未填写')
    Occupation = models.CharField(max_length=16, verbose_name='职业', null=True, default='未填写')
    partiality = models.CharField(max_length=3, verbose_name='偏好', null=True, default='未填写')
    experience = models.CharField(max_length=5, verbose_name='股龄', null=True, default='未填写')
    lever = models.CharField(max_length=3, verbose_name='杠杆', null=True, default='未填写')
    check_code = models.IntegerField(verbose_name='验证码', null=True)
    code_valid_time = models.IntegerField(verbose_name='验证码失效时间戳', null=True)
    class Meta:
        db_table = 'userprofiles'

class FingerPrint(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='用户请求指纹id')
    user = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, null=True, verbose_name='用户请求指纹')
    finger = models.CharField(max_length=30, verbose_name='用户请求指纹', null=True)
    class Meta:
        db_table = 'userfinger'