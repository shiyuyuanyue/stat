# Generated by Django 2.1.4 on 2020-01-09 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200108_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiles',
            name='password',
            field=models.CharField(max_length=160, verbose_name='密码'),
        ),
    ]