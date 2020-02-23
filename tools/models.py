from django.db import models


# Create your models here.
class Tools(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号', default=1)
    code = models.CharField(max_length=6, verbose_name='股票代码', db_index=True)
    title = models.CharField(max_length=12, verbose_name='股票名称')
    volume = models.IntegerField(verbose_name='成交量')
    date = models.DateField()
    bond = models.CharField(max_length=4, verbose_name='证券交易所')
    open = models.FloatField(max_length=8, verbose_name='开盘价')
    close = models.FloatField(max_length=8, verbose_name='收盘价')
    high = models.FloatField(max_length=8, verbose_name='最高价')
    low = models.FloatField(max_length=8, verbose_name='最低价')
    turnover = models.IntegerField(verbose_name='成交金额')
    rise = models.FloatField(max_length=6, verbose_name='上涨金额')
    gain = models.CharField(max_length=24, verbose_name='涨幅')

    class Meta:
        db_table = 'stockdata'
