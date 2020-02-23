# Generated by Django 2.1.4 on 2020-01-31 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0005_auto_20200128_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showdata',
            name='day_count',
            field=models.CharField(max_length=50, null=True, verbose_name='最高连涨出现次数'),
        ),
        migrations.AlterField(
            model_name='showdata',
            name='days',
            field=models.FloatField(max_length=50, null=True, verbose_name='最高连涨天数'),
        ),
        migrations.AlterField(
            model_name='showdata',
            name='desire_buy',
            field=models.FloatField(max_length=50, null=True, verbose_name='买入欲望植'),
        ),
        migrations.AlterField(
            model_name='showdata',
            name='score',
            field=models.FloatField(max_length=50, null=True, verbose_name='综合评分'),
        ),
    ]
