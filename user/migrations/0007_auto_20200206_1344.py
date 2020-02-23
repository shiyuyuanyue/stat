# Generated by Django 2.1.4 on 2020-02-06 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20200206_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiles',
            name='age',
            field=models.CharField(default='未填写', max_length=4, null=True, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='lever',
            field=models.CharField(default='未填写', max_length=3, null=True, verbose_name='杠杆'),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='partiality',
            field=models.CharField(default='未填写', max_length=3, null=True, verbose_name='偏好'),
        ),
    ]