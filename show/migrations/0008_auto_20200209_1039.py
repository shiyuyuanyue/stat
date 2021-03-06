# Generated by Django 2.1.4 on 2020-02-09 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0007_auto_20200207_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showdata',
            name='hot',
            field=models.FloatField(default=0, max_length=8, verbose_name='关注度'),
        ),
        migrations.AlterField(
            model_name='showdata',
            name='lkc',
            field=models.IntegerField(default=0, max_length=8, verbose_name='搜索热度'),
        ),
        migrations.AlterField(
            model_name='showdata',
            name='tt',
            field=models.IntegerField(default=0, max_length=8, verbose_name='累计追踪天数'),
        ),
    ]
