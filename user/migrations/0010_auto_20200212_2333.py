# Generated by Django 2.1.4 on 2020-02-12 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_fingerprint'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofiles',
            name='finger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.FingerPrint', verbose_name='用户请求指纹'),
        ),
        migrations.AlterField(
            model_name='fingerprint',
            name='finger',
            field=models.CharField(max_length=30, null=True, verbose_name='用户请求指纹'),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='check_code',
            field=models.IntegerField(null=True, verbose_name='验证码'),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='code_valid_time',
            field=models.IntegerField(null=True, verbose_name='验证码失效时间戳'),
        ),
    ]
