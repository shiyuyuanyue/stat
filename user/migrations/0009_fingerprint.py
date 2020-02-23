# Generated by Django 2.1.4 on 2020-02-12 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20200209_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='FingerPrint',
            fields=[
                ('id', models.AutoField(default=1, primary_key=True, serialize=False, verbose_name='用户请求指纹id')),
                ('finger', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.UserProfiles', verbose_name='用户请求指纹')),
            ],
            options={
                'db_table': 'userfinger',
            },
        ),
    ]