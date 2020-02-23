from django.db import models

# Create your models here.
from user.models import UserProfiles


class ShowData(models.Model):
    code = models.CharField(max_length=6, verbose_name='股票代码', primary_key=True)
    title = models.CharField(max_length=6, verbose_name='股票名称', null=True)
    #原始数据
    bond = models.CharField(max_length=4, verbose_name='证券交易所',null=True)
    open = models.FloatField(max_length=8, verbose_name='开盘价',null=True)
    close = models.FloatField(max_length=8, verbose_name='收盘价',null=True)
    high = models.FloatField(max_length=8, verbose_name='最高价',null=True)
    low = models.FloatField(max_length=8, verbose_name='最低价',null=True)
    volume = models.IntegerField(verbose_name='成交量',null=True)
    turnover = models.IntegerField(verbose_name='成交金额',null=True)
    rise = models.FloatField(max_length=6, verbose_name='上涨金额',null=True)
    gain = models.CharField(max_length=24, verbose_name='涨幅',null=True)
    #次生数据
    score = models.FloatField(max_length=50, verbose_name='综合评分', null=True)
    highest = models.CharField(max_length=50, verbose_name='历史最高', null=True)
    lowest = models.CharField(max_length=50, verbose_name='历史最低', null=True)
    average = models.CharField(max_length=50, verbose_name='历史均价', null=True)
    desire_buy = models.FloatField(max_length=50, verbose_name='买入欲望植', null=True)
    days = models.FloatField(max_length=50, verbose_name='最高连涨天数', null=True)
    day_count = models.CharField(max_length=50, verbose_name='最高连涨出现次数', null=True)
    lkc = models.IntegerField(verbose_name='搜索热度', default=0)
    beat = models.FloatField(max_length=8, verbose_name='击败率', null=True)
    rp = models.FloatField(max_length=8, verbose_name='上涨概率', null=True)
    fp = models.FloatField(max_length=8, verbose_name='下跌概率', null=True)
    hot = models.FloatField(max_length=8, verbose_name='关注度', default=0)
    tt = models.IntegerField(verbose_name='累计追踪天数', default=0)
    fans = models.ManyToManyField(UserProfiles)
    #AI数据
    linear_regression = models.CharField(max_length=50, verbose_name='线性回归预测', null=True)
    ridge_regression = models.CharField(max_length=50, verbose_name='岭回归预测', null=True)
    polynomial_regression = models.CharField(max_length=50, verbose_name='多项式回归预测', null=True)
    ai_prediction = models.CharField(max_length=50, verbose_name='AI预测', null=True)
    #命中相关
    hit = models.IntegerField(verbose_name='累计命中次数', default=0)
    hit_r = models.FloatField(max_length=8, verbose_name='命中率', default=0)
    pre_num = models.IntegerField(verbose_name='预测次数', default=0)
    #预测准确率
    acc = models.FloatField(max_length=8, verbose_name='个股准确率', default=0)
    #看张看跌
    view_up = models.IntegerField(verbose_name='看涨人数', default=1)
    view_down = models.IntegerField(verbose_name='看跌人数', default=1)
    up_pro = models.FloatField(max_length=8, verbose_name='看涨比例', default=50)
    down_pro = models.FloatField(max_length=8, verbose_name='看跌比例', default=50)
    #用户画像
    date = models.DateField(verbose_name='最后更新日期', null=True)
    nlp = models.CharField(max_length=400, verbose_name='情感分析NLP关键字', null=True)
    prosex = models.CharField(max_length=20, verbose_name='男女比例', null=True)
    proage = models.CharField(max_length=60, verbose_name='年龄比例', null=True)
    proinc = models.CharField(max_length=120, verbose_name='收入比例', null=True)
    proexp = models.CharField(max_length=100, verbose_name='经验比例', null=True)
    prolev = models.CharField(max_length=20, verbose_name='杠杆比例', null=True)
    propre = models.CharField(max_length=20, verbose_name='杠杆比例', null=True)
    proocc = models.CharField(max_length=100, verbose_name='杠杆比例', null=True)

    class Meta:
        db_table = 'showdata'

#统计数据
class Stats(models.Model):
    id = models.AutoField(primary_key=True)
    allnum = models.IntegerField( verbose_name='原始数据总条数', default=0)
    stnum = models.IntegerField( verbose_name='股票总数', default=0)
    mknum = models.IntegerField( verbose_name='生成数据总个数', default=0)
    usernum = models.IntegerField(verbose_name='用户总数', default=0)
    ttt = models.IntegerField(verbose_name='累计追踪次数', default=0)
    allacc = models.FloatField(max_length=8, verbose_name='准确率', default=0)
    date = models.DateField(verbose_name='统计日期')

    class Meta:
        db_table = 'statsdata'
