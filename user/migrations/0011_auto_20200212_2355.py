# Generated by Django 2.1.4 on 2020-02-12 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20200212_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofiles',
            name='finger',
        ),
        migrations.AlterField(
            model_name='fingerprint',
            name='finger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.UserProfiles', verbose_name='用户请求指纹'),
        ),
    ]
