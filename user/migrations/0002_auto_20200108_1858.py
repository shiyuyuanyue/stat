# Generated by Django 2.1.4 on 2020-01-08 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiles',
            name='Occupation',
            field=models.CharField(max_length=4, null=True, verbose_name='职业'),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='age',
            field=models.IntegerField(max_length=3, null=True, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='avatar',
            field=models.ImageField(max_length=1000, null=True, upload_to='statoc/avatar/%Y/%m/%d/', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='experience',
            field=models.CharField(max_length=3, null=True, verbose_name='股龄'),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='gender',
            field=models.CharField(max_length=4, null=True, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='lever',
            field=models.CharField(max_length=1, null=True, verbose_name='杠杆'),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='partiality',
            field=models.CharField(max_length=2, null=True, verbose_name='偏好'),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='salary',
            field=models.CharField(max_length=12, null=True, verbose_name='工资'),
        ),
    ]
