# Generated by Django 2.1.4 on 2020-01-27 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_auto_20200107_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tools',
            name='bond',
            field=models.CharField(max_length=4, verbose_name='证券交易所'),
        ),
        migrations.AlterField(
            model_name='tools',
            name='close',
            field=models.FloatField(max_length=8, verbose_name='收盘价'),
        ),
        migrations.AlterField(
            model_name='tools',
            name='code',
            field=models.CharField(db_index=True, max_length=6, verbose_name='股票代码'),
        ),
        migrations.AlterField(
            model_name='tools',
            name='high',
            field=models.FloatField(max_length=8, verbose_name='最高价'),
        ),
        migrations.AlterField(
            model_name='tools',
            name='low',
            field=models.FloatField(max_length=8, verbose_name='最低价'),
        ),
        migrations.AlterField(
            model_name='tools',
            name='open',
            field=models.FloatField(max_length=8, verbose_name='开盘价'),
        ),
        migrations.AlterField(
            model_name='tools',
            name='title',
            field=models.CharField(max_length=12, verbose_name='股票名称'),
        ),
        migrations.AlterField(
            model_name='tools',
            name='turnover',
            field=models.IntegerField(max_length=20, verbose_name='成交金额'),
        ),
        migrations.AlterField(
            model_name='tools',
            name='volume',
            field=models.IntegerField(max_length=20, verbose_name='成交量'),
        ),
    ]