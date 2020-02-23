# Create your views here.
from time import sleep
from django.http import JsonResponse
from show.models import ShowData, Stats
from tools.models import Tools
import sklearn.linear_model as lm
import numpy as np
import datetime
import sklearn.pipeline as pl
import sklearn.preprocessing as sp
from jieba.analyse import *
import requests
from lxml import etree
from user.models import UserProfiles
# from fake_useragent import UserAgent


class ShowStockData:
    """
    股票数据展示页面相关数据计算
    """

    def __init__(self, code):
        # 指定股票代码
        self.code = code
        # 获取指定股票代码的全量记录
        self.datas = Tools.objects.filter(code=self.code).order_by('-date')  # 按时间倒序
        # 获取全量最高价
        self.list_high = [data.high for data in self.datas]
        # 获取全量最低价
        self.list_low = [data.low for data in self.datas if data.low > 0]
        # 获取全量上涨金额
        self.list_rise = [data.rise for data in self.datas]
        # 交易所
        if str(code)[0] in ['2', '5', '6', '9']:
            self.bond = 'SH上证'
        else:
            self.bond = 'SZ深证'
        #删除污染数据
        newdt = self.datas[0]
        self.close = newdt.close
        self.high = newdt.high
        self.low = newdt.low
        self.volume = newdt.volume
        self.turnover = newdt.turnover
        self.rise = newdt.rise
        self.gain = newdt.gain
        self.open = newdt.open
        if not self.open:
            print(self.code,self.close,'发现为空')
            sleep(6000)
    # list_key, day_count, desire_buy
    def desire_buy(self):
        if self.datas:
            high, low, avg = max(self.list_high), min(self.list_low), sum(self.list_high) / len(self.list_high)
            # 最新一条的收盘价
            new_data = self.datas[0]
            newclose = new_data.close
            # low_dif = 最新一条收盘价-历史最低价/历史最低价 越小能量越大
            lof = (newclose - low) / low
            # 与历史均价差比越小能量越大
            avq = (newclose - avg) / avg
            # 历史最大连涨次数
            list_count = [2]
            count = 1
            for i in range(len(self.list_rise) - 1):
                if float(self.list_rise[i]) > 0 and float(self.list_rise[i + 1]) > 0:
                    count += 1
                    list_count.append(count)
                else:
                    count = 1
                    continue
            if not list_count:
                print(self.datas[0].code)
            max_count = max(list_count)
            # 连涨事件出现次数最多的{天数：次数}
            dict_count = {}
            for i in range(2, max_count + 1):
                # 字典{天数：次数}
                dict_count[i] = list_count.count(i)
            # 获取次数最大的天数列表[连涨2天，连涨3天]
            list_key = [k for k, v in dict_count.items() if k == max(dict_count.keys())]
            # 次数
            day_count = [v for k, v in dict_count.items() if k == max(dict_count.keys())]
            # 获取历史连涨相等的天数数据
            somedays = self.datas[:list_key[0]]
            r = 0
            g = 0
            for data in somedays:
                #涨幅去掉%，转化成小数 >=0 表示上涨
                if float(data.gain[:-1]) >= 0:
                    #上涨次数+1
                    r += 1
                else:
                    # 否则下跌次数+1
                    g += 1
            # 近期上涨天数/历史最高连涨天数(下跌概率)
            arq = round((r / list_key[0])*100,2)
            # 购买欲望值
            desire_buy = 1 - lof*0.33 - avq * 0.33 - r / list_key[0]*0.33
            return list_key, day_count, desire_buy, newclose, high, low, avg, arq
        else:
            print(self.code, '空')

    # 获取nlp
    def getnlp(self):
        # 获取股票代码
        code = self.code
        # 生成爬虫请求链接
        url = 'http://guba.eastmoney.com/list,{}.html'.format(code)
        # 解析页面
        #ua = UserAgent() ua.random
        res = requests.get(url=url, headers={'UserAgent':'Mozilla/5.0'})
        html = res.text
        parse_html = etree.HTML(html)
        list_span = parse_html.xpath('//span[@class="l3 a3"]//a/@title')[8:]
        # 提取文本
        data = ''
        for span in list_span:
            data += span
        # 提取TF-idf关键字和权重
        tfwords = ''
        for keyword, weight in extract_tags(data, withWeight=True):
            tfwords += keyword + '(' + str(round(weight, 2)) + '),'
        # 提取TextRank关键字和权重
        trwords = ''
        for keyword, weight in textrank(data, withWeight=True):
            trwords += keyword + '(' + str(round(weight, 2)) + '),'
        nlp = tfwords + '/' + trwords
        return nlp

    # 三种线性回归预测算法：linear_result,ridge_result,pro_result,ai_prediction
    def linear_regression(self):
        # 创建全量收盘价列表
        list_datas = []
        # 将全量收盘价和日期添加至列表
        for data in self.datas:
            list_datas.append(data.close)
        # 将列表元素索引反转 升序
        list_datas_new = list(reversed(list_datas))
        # 生成收盘价array数组多行1列
        y = np.array(list_datas_new)
        # 生成全量收盘价array数组多行1列
        x = np.arange(1, len(list_datas_new) + 1).reshape(-1, 1)
        # 创建线性回归模型
        model = lm.LinearRegression()
        # 训练
        model.fit(x, y)
        # 预测
        linear_result01 = model.predict(np.array(len(list_datas_new) + 1).reshape(-1, 1))[0]
        #合理化 控制不超过10%涨跌幅
        linear_result = ((linear_result01 - self.close)/linear_result01)*0.1*self.close + self.close
        # 创建岭回归模型
        model_r = lm.Ridge(300, fit_intercept=True, max_iter=10)
        # 训练
        model_r.fit(x, y)
        # 预测
        ridge_result01 = model_r.predict(np.array(len(list_datas_new) + 1).reshape(-1, 1))[0]
        #合理化 控制不超过10%涨跌幅
        ridge_result = ((ridge_result01 - self.close) / ridge_result01) * 0.1 * self.close + self.close
        # 创建多项式回归模型
        model_p = pl.make_pipeline(sp.PolynomialFeatures(3), lm.LinearRegression())
        # 训练
        model_p.fit(x, y)
        # 预测
        pr_result01 = model_p.predict(np.array(len(list_datas_new) + 1).reshape(-1, 1))[0]
        pr_result = ((pr_result01 - self.close) / pr_result01) * 0.1 * self.close + self.close
        # pro_result：三种预测结果平均数 消除多项式回归过拟合
        p_result = (linear_result + ridge_result + pr_result) / 3
        #再次求平均 进一步消除多项式回归过拟合
        pro_result =  (linear_result + ridge_result + p_result) / 3
        # ai_prediction:pro_result + linear_result + ridge_result平均数 二次消除过拟合
        ai_prediction = (pro_result + linear_result + ridge_result) / 3
        #个股准确率算法
        code_01 = self.close
        acc01 = abs(linear_result-code_01)/code_01
        acc02 = abs(ridge_result-code_01)/code_01
        acc03 = abs(pro_result-code_01)/code_01
        acc04 = abs(ai_prediction-code_01)/code_01
        acc = round(((4-acc01-acc02-acc03-acc04)/4)*100,2)
        return linear_result, ridge_result, pro_result, ai_prediction,acc


# 输入列表 输出出现次数最多元素的占比
def makepro(list):
    max_item = max(list, key=list.count)
    max_item_count = list.count(max_item)
    float_pro = max_item_count / len(list) * 100
    pro = max_item + '/' + str(round(float_pro, 2)) + '%'
    return pro


# 成功股票展示页面数据
def makedatas(request):
    # 获取全量统计数据queryset对象
    statdatas = Stats.objects.all()[0]
    # 获取全量原始股票数据queryset对象列表
    tooldatas = Tools.objects.order_by("-id")[0]
    # 获取全量生成股票数据queryset对象列表
    stockdatas = ShowData.objects.all()
    # 获取全量用户信息数据queryset对象列表
    userdatas = UserProfiles.objects.all()
    #累计追踪次数 每次叠加 股票总数
    statdatas.ttt += len(stockdatas)
    #赋值
    statdatas.allnum = tooldatas.id
    statdatas.stnum = len(stockdatas)
    statdatas.usernum = len(userdatas)
    #生成新数据数量 = 总股票数 * 29 + 6
    statdatas.mknum = len(stockdatas) * 29 + 6
    #执行时间 （统计日期）
    statdatas.date = datetime.date.today()
    #执行更新
    statdatas.save()
    #遍历单条queryset对象 可切片stockdatas控制增量更新
    #捕获爬虫异常的股票代码
    list_error = []
    #计数器打印在终端
    count = 2284
    for stockdata in stockdatas[2284:]:
        # 获取指定股票代码对象
        code = stockdata.code
        showdata = ShowStockData(code)
        # 获取指定股票代码对象的list_key,day_count,desire_buy,newclose,high,low,avg
        list_key, day_count, desire_buy, newclose, high, low, avg, arq = showdata.desire_buy()
        # 拼接最大连涨出现次数
        days = list_key[0]
        # 获取指定股票代码对象的linear_result, ridge_result, pro_result, ai_prediction
        linear_result, ridge_result, pro_result, ai_prediction,acc = showdata.linear_regression()
        # 综合得分score 算法
        score1 = desire_buy + (ai_prediction - newclose) / newclose
        score = round(score1, 2)
        # rp上涨概率算法
        rp = 100 - arq
        # 获取粉丝数量(关注度)
        list_fans = stockdata.fans.all()
        #如果有粉丝 开始计算男女占比
        hot = len(list_fans)
        m_fans = [fans for fans in list_fans if fans.gender == '男']
        float_mp = round(len(m_fans) / hot * 100, 2)
        # 66.66%
        mp = str(float_mp) + '%'
        # 33.34%
        wp = str(100 - float_mp) + '%'
        # 用/拼接
        prosex = mp + '/' + wp
        # 年龄占比最高算法 proage
        list_fans_age = [fans.age for fans in list_fans]
        list_fans_inc = [fans.salary for fans in list_fans]
        list_fans_exp = [fans.experience for fans in list_fans]
        list_fans_lev = [fans.lever for fans in list_fans]
        list_fans_pre = [fans.partiality for fans in list_fans]
        list_fans_occ = [fans.Occupation for fans in list_fans]
        proage = makepro(list_fans_age)
        proinc = makepro(list_fans_inc)
        proexp = makepro(list_fans_exp)
        prolev = makepro(list_fans_lev)
        propre = makepro(list_fans_pre)
        proocc = makepro(list_fans_occ)

        # 保存相关数据到数据库
        data = ShowData.objects.get(code=code)
        data.score = score
        data.highest = high
        data.lowest = low
        data.average = round(avg, 2)
        data.desire_buy = round(desire_buy, 2)
        #相关预测 保存
        data.linear_regression = round(linear_result, 2)
        data.ridge_regression = round(ridge_result, 2)
        data.polynomial_regression = round(pro_result, 2)
        data.ai_prediction = round(ai_prediction, 2)
        data.acc = acc
        data.tt += 1  # 累计追踪天数+1
        data.pre_num = data.tt*4 #累计预测次数
        #计算命中率
        if round(linear_result, 2) == data.close :
            data.hit += 1 #累计命中次数+1
        if round(ridge_result, 2) == data.close :
            data.hit += 1 #累计命中次数+1
        if round(pro_result, 2) == data.close :
            data.hit += 1 #累计命中次数+1
        if round(ai_prediction, 2) == data.close :
            data.hit += 1 #累计命中次数+1
        # 命中率
        data.hit_r = round((data.hit/data.pre_num)*100,2)
        #最高连涨天数
        data.days = days
        #最高连涨出现次数
        data.day_count = day_count[0]
        # data.lkc = 在show.views.py 里已经保存
        # data.beat = 在全量数据更新之后再计算
        data.rp = rp
        data.fp = arq
        data.hot = hot
        # data.fans = 多对多关联了UserProFiles
        data.date = datetime.date.today()
        try:
            data.nlp = showdata.getnlp()
        except Exception as e:
            print(e,code,'爬取出现异常')
            list_error.append(code)
        #用户画像数据保存
        data.prosex = prosex
        data.proage = proage
        data.proinc = proinc
        data.proexp = proexp
        data.prolev = prolev
        data.propre = propre
        data.proocc = proocc
        # 股票原始数据保存
        data.gain = showdata.gain
        data.bond = showdata.bond
        data.open = showdata.open
        data.close = showdata.close
        data.high = showdata.high
        data.low = showdata.low
        data.volume =showdata.volume
        data.turnover =showdata.turnover
        data.rise = showdata.rise
        #看涨看跌每日更新清零
        data.view_down = 0
        data.view_up = 0
        data.up_pro = 0
        data.down_pro = 0
        count+=1
        print(count, code, data.bond, 'hit_r', round((data.hit / data.pre_num) * 100, 2), 'acc', acc, 'ok', )
        try:
            data.save()
        except Exception as e:
            print(e)

    # beat 击败率算法(所有数据更新完毕再算击败率)
    list_scores = []  # 获取全量score得分列表
    list_acc = [] #获取全量准确率列表
    for sdata in stockdatas:
        list_scores.append(sdata.score)
        list_acc.append(sdata.acc)
    #所有个股准确率的平均数
    allacc = np.mean(list_acc)
    # 获取全量QUERYSET对象
    for sd in stockdatas:
        # 获取小于sd得分列表
        list_news = [score for score in list_scores if sd.score > score]
        # 计算击败率
        beat = len(list_news) / len(list_scores)
        # 保存至数据库
        sd.beat = round(beat*100,2)#击败率
        sd.save()
    #保存全局准确率
    statdatas.allacc = round(allacc,2)#飘黄没关系 已测试
    statdatas.save()
    # 获取全量score并缩放至0-10000
    make_score()
    print(list_error,'本次追踪丢失，请重新对这几支股票进行追踪')
    result = {'code': 200}
    return JsonResponse(result)


# 获取全量score并缩放至0-100
def make_score():
    # 获取全量数据queryset对象
    stockdatas = ShowData.objects.all().order_by('code')
    # 创建全量score列表
    list_score = []
    # 创建全量desire_buy列表
    list_desire_buy = []
    for stock_data in stockdatas:
        list_score.append(float(stock_data.score))
        list_desire_buy.append(float(stock_data.desire_buy))
    # 把全量score列表转换成array数组并改变shape为多行1列
    ary_score = np.array(list_score, dtype='float64').reshape(-1, 1)
    # 同上
    ary_desire_buy = np.array(list_desire_buy).reshape(-1, 1)
    # 创建缩放器对象
    mms = sp.MinMaxScaler(feature_range=(1, 100))
    # 缩放并输出新数组
    mms_score = mms.fit_transform(ary_score)
    mms_desire_buy = mms.fit_transform(ary_desire_buy)
    # 转置为一行多列
    list_mms_score = mms_score.T
    list_mms_desire_buy = mms_desire_buy.T
    # 重新保存至数据库
    for i in range(len(stockdatas)):
        stockdatas[i].score = round(list_mms_score[0][i],2)
        stockdatas[i].desire_buy = round(list_mms_desire_buy[0][i],2)
        stockdatas[i].save()
        print(stockdatas[i].code, '综合评分更新完毕')
    return JsonResponse({'code': 200})
