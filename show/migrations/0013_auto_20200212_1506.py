# Generated by Django 2.1.4 on 2020-02-12 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0012_showdata_volume'),
    ]

    operations = [
        migrations.AddField(
            model_name='showdata',
            name='down_pro',
            field=models.FloatField(default=50, max_length=8, verbose_name='看跌比例'),
        ),
        migrations.AddField(
            model_name='showdata',
            name='hit',
            field=models.IntegerField(default=0, max_length=8, verbose_name='累计命中次数'),
        ),
        migrations.AddField(
            model_name='showdata',
            name='hit_r',
            field=models.FloatField(default=0, max_length=8, verbose_name='命中率'),
        ),
        migrations.AddField(
            model_name='showdata',
            name='pre_num',
            field=models.IntegerField(default=0, max_length=8, verbose_name='预测次数'),
        ),
        migrations.AddField(
            model_name='showdata',
            name='up_pro',
            field=models.FloatField(default=50, max_length=8, verbose_name='看涨比例'),
        ),
        migrations.AddField(
            model_name='showdata',
            name='view_down',
            field=models.IntegerField(default=1, max_length=8, verbose_name='看跌人数'),
        ),
        migrations.AddField(
            model_name='showdata',
            name='view_up',
            field=models.IntegerField(default=1, max_length=8, verbose_name='看涨人数'),
        ),
    ]
