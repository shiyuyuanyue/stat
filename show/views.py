import datetime
import json
from django.db.models import Q
from django.http import JsonResponse
from show.models import ShowData, Stats
from tools.models import Tools
from user.models import UserProfiles, FingerPrint
from tool.login_check import login_check


@login_check('POST', 'DELETE','PUT')
def search_api(request, code=None, kw=None):
    # 校验请求方法
    if request.method == 'GET':
        # 校验是否存在查询字符串
        if not request.GET.keys():
            Tools.objects.all()
            # 获取全量queryset对象 按socre,desire_buy,days 倒序
            list_score_datas = ShowData.objects.all().order_by('-score')
            list_desire_buy_datas = ShowData.objects.all().order_by('-desire_buy')
            list_days_datas = ShowData.objects.all().order_by('-days')
            list_hot = ShowData.objects.all().order_by('-hot')#关注排行
            list_lkc = ShowData.objects.all().order_by('-lkc')#搜索排行
            list_acc = ShowData.objects.all().order_by('-acc')#准确率排行
            list_view_up = ShowData.objects.all().order_by('-view_up')#看涨排行
            # 创建列表 装10条数据
            list_top_score = []
            list_top_desire_buy = []
            list_top_days = []
            list_top_hot = []
            list_top_lkc = []
            list_top_acc = []
            list_top_view_up = []
            # 排名
            num_days = 0
            num_desire_buy = 0
            num_score = 0
            num_hot = 0
            num_lkc = 0
            num_acc = 0
            num_view_up = 0
            # 获取view_up看涨排行前十名数据
            for data in list_view_up[:10]:
                dict_top_datas = {}
                num_view_up += 1
                dict_top_datas['code'] = data.code
                dict_top_datas['title'] = data.title
                dict_top_datas['score'] = data.up_pro
                if num_view_up < 10:
                    dict_top_datas['num'] = '%02d' % num_view_up
                else:
                    dict_top_datas['num'] = num_view_up
                list_top_view_up.append(dict_top_datas)
            # 获取acc准确率排行前十名数据
            for data in list_acc[:10]:
                dict_top_datas = {}
                num_acc += 1
                dict_top_datas['code'] = data.code
                dict_top_datas['title'] = data.title
                dict_top_datas['score'] = data.acc
                if num_acc < 10:
                    dict_top_datas['num'] = '%02d' % num_acc
                else:
                    dict_top_datas['num'] = num_acc
                list_top_acc.append(dict_top_datas)
            # 获取lkc搜索排行前十名数据
            for data in list_lkc[:10]:
                dict_top_datas = {}
                num_lkc += 1
                dict_top_datas['code'] = data.code
                dict_top_datas['title'] = data.title
                dict_top_datas['score'] = data.lkc
                if num_lkc < 10:
                    dict_top_datas['num'] = '%02d' % num_lkc
                else:
                    dict_top_datas['num'] = num_lkc
                list_top_lkc.append(dict_top_datas)

            # 获取hot关注度前十名数据
            for data in list_hot[:10]:
                dict_top_datas = {}
                num_hot += 1
                dict_top_datas['code'] = data.code
                dict_top_datas['title'] = data.title
                dict_top_datas['score'] = data.hot
                if num_hot < 10:
                    dict_top_datas['num'] = '%02d' % num_hot
                else:
                    dict_top_datas['num'] = num_hot
                list_top_hot.append(dict_top_datas)


            # 获取score前十名数据
            for data in list_score_datas[:10]:
                dict_top_datas = {}
                num_score += 1
                dict_top_datas['code'] = data.code
                dict_top_datas['title'] = data.title
                dict_top_datas['score'] = data.score
                if num_score < 10:
                    dict_top_datas['num'] = '%02d' % num_score
                else:
                    dict_top_datas['num'] = num_score
                list_top_desire_buy.append(dict_top_datas)
            # 获取desire_buy前十名数据
            for data in list_desire_buy_datas[:10]:
                dict_top_datas = {}
                num_desire_buy += 1
                dict_top_datas['code'] = data.code
                dict_top_datas['title'] = data.title
                dict_top_datas['score'] = data.desire_buy
                if num_desire_buy < 10:
                    dict_top_datas['num'] = '%02d' % num_desire_buy
                else:
                    dict_top_datas['num'] = num_desire_buy
                list_top_score.append(dict_top_datas)
            # 获取days前十名数据
            for data in list_days_datas[:10]:
                dict_top_datas = {}
                num_days += 1
                dict_top_datas['code'] = data.code
                dict_top_datas['title'] = data.title
                dict_top_datas['score'] = data.days
                if num_days < 10:
                    dict_top_datas['num'] = '%02d' % num_days
                else:
                    dict_top_datas['num'] = num_days
                list_top_days.append(dict_top_datas)

            result = {'code': 200, 'data': [list_top_score, list_top_desire_buy, list_top_days,list_top_hot,list_top_lkc,list_top_acc,list_top_view_up]}
            return JsonResponse(result)
        else:
            # 限制查询字符串必须为1
            if len(request.GET.keys()) > 1:
                result = {'code': 3003, 'error': '传参数量超限'}
                return JsonResponse(result)
            else:
                # 提取查询字符串
                for key in request.GET.keys():
                    # 检验查询字符串是否合法
                    if key not in ['kw', 'code','ost_user','stats']:
                        result = {'code': 3002, 'error': '非法参数'}
                        return JsonResponse(result)
                    else:
                        # kw表示搜索提示 发来的请求
                        if key == 'kw':
                            kw = request.GET.get('kw')
                            # 校验kw是否为数字（股票代码）
                            if kw.isdigit():
                                # 模糊查询匹配
                                listdatas = ShowData.objects.filter(code__icontains=(kw.strip()))
                                # 创建模糊查询返回的股票代码和名称列表
                                likewords = []
                                # 如果结果>5只保留前5条
                                if len(listdatas) > 5:
                                    listdatas = listdatas[:5]
                                    for listdata in listdatas:
                                        # 模糊查询结果添加至列表
                                        likewords.append((listdata.code, listdata.title))
                                    result = {'code': 3000, 'data': {'likewords': likewords}}
                                    return JsonResponse(result)
                                else:
                                    # 如果模糊查询条数<5则全部添加至列表
                                    for listdata in listdatas:
                                        likewords.append((listdata.code, listdata.title))
                                    result = {'code': 3000, 'data': {'likewords': likewords}}
                                    return JsonResponse(result)
                            else:
                                # 否则非数字，执行字符串模糊查询
                                listdatas = ShowData.objects.filter(title__icontains=(kw.strip()))
                                # 如果字符串模糊查询无结果
                                if not listdatas:
                                    result = {'code': 3004, 'error': "该关键词无匹配结果"}
                                    return JsonResponse(result)
                                else:
                                    # 如果字符串模糊查询结果>5只保留前5条
                                    if len(listdatas) > 5:
                                        # 创建模糊查询返回的股票代码和名称列表
                                        likewords = []
                                        # 只保留前5条
                                        for listdata in listdatas[:5]:
                                            # 添加至列表
                                            likewords.append((listdata.code, listdata.title))
                                        result = {'code': 3000, 'data': {'likewords': likewords}}
                                        return JsonResponse(result)
                                    else:
                                        # 否则模糊查询结果<5，全部添加至列表
                                        likewords = []
                                        for listdata in listdatas:
                                            likewords.append((listdata.code, listdata.title))
                                        result = {'code': 3000, 'data': {'likewords': likewords}}
                                        return JsonResponse(result)
                        # 如果查询字符串是code，则返回搜索结果页面相关数据
                        elif key == 'code':
                            code = request.GET.get('code')  # 获取code值
                            if code == 'allstatsdatas':#只获取统计数据
                                stats = Stats.objects.get(id=1)
                                # 获取原始数据总条数
                                allnum = stats.allnum
                                # 获取股票总条数
                                stnum = stats.stnum
                                # 获取生成数据总条数
                                mknum = stats.mknum
                                # 获取用户总数
                                usernum = stats.usernum
                                # 获取全局累计追踪次数
                                ttt = stats.ttt
                                # 获取全局数据更新日期
                                up_date = stats.date
                                # 全局准确率
                                allacc = stats.allacc
                                stats_dict = {}
                                stats_dict['allnum'] = allnum
                                stats_dict['stnum'] = stnum
                                stats_dict['mknum'] = mknum
                                stats_dict['usernum'] = usernum
                                stats_dict['ttt'] = ttt
                                stats_dict['up_date'] = up_date
                                stats_dict['allacc'] = allacc
                                result = {'code':200,'data':stats_dict}
                                return JsonResponse(result)
                            # 获取股票代码全量模糊查询匹配结果
                            datas = ShowData.objects.filter(Q(title__icontains=(code)) | Q(code__icontains=(code)))
                            # 如果匹配不到
                            if not datas:
                                result = {'code': 3005, 'error': '股票信息不存在'}
                                return JsonResponse(result)
                            else:
                                stats = Stats.objects.get(id=1)
                                # 获取原始数据总条数
                                allnum = stats.allnum
                                # 获取股票总条数
                                stnum = stats.stnum
                                # 获取生成数据总条数
                                mknum = stats.mknum
                                # 获取用户总数
                                usernum = stats.usernum
                                # 获取全局累计追踪次数
                                ttt = stats.ttt
                                # 获取全局数据更新日期
                                up_date = stats.date
                                #全局准确率
                                allacc = stats.allacc
                                stats_dict = {}
                                stats_dict['allnum'] = allnum
                                stats_dict['stnum'] = stnum
                                stats_dict['mknum'] = mknum
                                stats_dict['usernum'] = usernum
                                stats_dict['ttt'] = ttt
                                stats_dict['up_date'] = up_date
                                stats_dict['allacc'] = allacc
                                # 返回索引股票代码匹配的的全量数据 列表
                                dt = datas[0] # 返回前1条
                                dt.lkc += 1  # 搜索热度+1
                                dt.save()
                                print(dt.gain)
                                data = {
                                    'code': dt.code,
                                    'title': dt.title,
                                    'score': dt.score,
                                    'highest': dt.highest,
                                    'lowest': dt.lowest,
                                    'average': dt.average,
                                    'desire_buy': dt.desire_buy,
                                    'linear_regression': dt.linear_regression,
                                    'ridge_regression': dt.ridge_regression,
                                    'polynomial_regression': dt.polynomial_regression,
                                    'ai_prediction': dt.ai_prediction,
                                    'days': dt.days,
                                    'day_count': dt.day_count,
                                    'lkc': dt.lkc,
                                    'beat': dt.beat,
                                    'rp': dt.rp,
                                    'fp': dt.fp,
                                    'hot': dt.hot,
                                    'tt': dt.tt,
                                    'date': dt.date,
                                    'nlp': dt.nlp,
                                    'prosex': dt.prosex,
                                    'proage': dt.proage,
                                    'proinc': dt.proinc,
                                    'proexp': dt.proexp,
                                    'prolev': dt.prolev,
                                    'propre': dt.propre,
                                    'proocc': dt.proocc,

                                    'bond':dt.bond ,#交易所
                                    'open':dt.open,
                                    'close':dt.close,
                                    'high':dt.high,
                                    'low':dt.low,
                                    'volume':dt.volume,#成交量
                                    'turnover':dt.turnover,#成交金额
                                    'rise':dt.rise,#上涨金额
                                    'gain':dt.gain,# 涨幅

                                    'pre_num':dt.pre_num, #累计预测天数
                                    'hit':dt.hit,#累计命中次数
                                    'hit_r':dt.hit_r,#命中率
                                    'acc': dt.acc,# 准确率

                                    'view_up':dt.view_up,#看涨看跌
                                    'view_down':dt.view_down,
                                    'up_pro':dt.up_pro,#看涨比例
                                    'down_pro':dt.down_pro#看跌比例
                                }
                                result = {'code': 3000, 'data': data,'stats':stats_dict}
                                return JsonResponse(result)

                        #负责查询字符串是关注者ost_user
                        else:
                            ost_user = request.GET.get('ost_user')
                            user = UserProfiles.objects.get(username = ost_user)
                            stocks = user.showdata_set.all()
                            list_datas = []
                            for stock in stocks:
                                data = {}
                                data['code'] = stock.code
                                data['title'] = stock.title
                                data['score'] = stock.score
                                data['highest'] = stock.highest
                                data['lowest'] = stock.lowest
                                data['average'] = stock.average
                                data['desire_buy'] = stock.desire_buy
                                data['ai_prediction'] = stock.ai_prediction
                                data['beat'] = stock.beat
                                data['lkc'] = stock.lkc
                                data['rp'] = stock.rp
                                data['date'] = stock.date
                                data['days'] = stock.days
                                list_datas.append(data)
                            result = {"code":3000,"data":list_datas}
                            return JsonResponse(result)
    # POST添加自选股
    elif request.method == 'POST':
        json_str = request.body
        if not json_str:
            result = {"code": 601, "error": "请求数据不能为空"}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        # 获取请求code和username
        code = json_obj['code']
        username = json_obj['username']
        # 校验请求 用户 是否为空
        if not username:
            result = {"code": 602, "error": "用户名不能为空"}
            return JsonResponse(result)
        # 校验请求 股票代码 是否为空
        if not code:
            result = {'code': 3005, 'error': '股票代码不能为空'}
            return JsonResponse(result)
        # get会抛异常 捕获
        try:
            user = UserProfiles.objects.get(username=username)
        except Exception:
            user = None
            # 如果没有查询到该用户
            if not user:
                result = {"code": 503, "error": "用户名不存在"}
                return JsonResponse(result)
        # get会抛异常 捕获
        try:
            optcode = ShowData.objects.get(code=code)
        except Exception:
            optcode = None
            # 如果没有查询到股票代码
        if not optcode:
            result = {'code': 3005, 'error': '股票信息不存在'}
            return JsonResponse(result)
            # 添加多对多关联
        optcode.fans.add(user)
        # 返回全量 该用户关注的股票数据列表
        result = {"code": 3000}
        return JsonResponse(result)

    # PUT看张看跌
    elif request.method == 'PUT':
        json_str = request.body
        if not json_str:
            result = {"code": 601, "error": "请求数据不能为空"}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        # 获取请求code和username
        code = json_obj['code']
        username = json_obj['username']
        view = json_obj['view']
        # 校验请求 用户 是否为空
        if not username:
            result = {"code": 602, "error": "用户名不能为空"}
            return JsonResponse(result)
        # 校验请求 股票代码 是否为空
        if not code:
            result = {'code': 3005, 'error': '股票代码不能为空'}
            return JsonResponse(result)
        #校验观点 是否为空
        if not view or view not in [2,1]:
            result = {'code': 3006, 'error': '观点参数错误，必须是1/2'}
            return JsonResponse(result)
        # get会抛异常 捕获
        try:
            user = UserProfiles.objects.get(username=username)
        except Exception:
            user = None
            # 如果没有查询到该用户
        if not user:
            result = {"code": 503, "error": "用户名不存在"}
            return JsonResponse(result)
        # get会抛异常 捕获
        try:
            viewcode = ShowData.objects.get(code=code)
        except Exception:
            viewcode = None
            # 如果没有查询到股票代码
        if not viewcode:
            result = {'code': 3005, 'error': '股票信息不存在'}
            return JsonResponse(result)
        #生成请求指纹 校验当日表态次数
        # 生成指纹 zhangsan60051920200201
        finger_str = username + str(code) + datetime.date.today().strftime("%Y%m%d")
        #查询指纹
        fingers = FingerPrint.objects.filter(finger=finger_str)
        # 如果指纹已存在
        if fingers:
            result = {'code': 3004, 'error': '您今日对该股票已表达看法，请明天再来'}
            return JsonResponse(result)
        #指纹不存在 1 看涨+1
        if view == 1:
            #看涨+1
            viewcode.view_up += 1
            #创建一个新指纹
            FingerPrint.objects.create(finger=finger_str,user=user)
        #0 看跌+1
        elif view == 2:
            #看跌+1
            viewcode.view_down += 1
            #创建一个新指纹
            FingerPrint.objects.create(finger=finger_str,user=user)
        # 看涨概率
        up_pro = round(viewcode.view_up / (viewcode.view_up + viewcode.view_down) * 100, 2)
        #看跌概率
        down_pro = 100 - up_pro
        #保存
        viewcode.up_pro = up_pro
        viewcode.down_pro = down_pro
        viewcode.save()
        # 返回全量 该用户关注的股票数据列表
        result = {"code": 3000,'error':'发表成功'}
        return JsonResponse(result)

    elif request.method == 'DELETE':
        json_str = request.body
        if not json_str:
            result = {"code": 601, "error": "请求数据不能为空"}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        # 获取请求code和username
        code = json_obj['code']
        username = json_obj['username']
        # 校验请求 用户 是否为空
        if not username:
            result = {"code": 602, "error": "用户名不能为空"}
            return JsonResponse(result)
        # 校验请求 股票代码 是否为空
        if not code:
            result = {'code': 3005, 'error': '股票代码不能为空'}
            return JsonResponse(result)

        # get会抛异常 捕获
        try:
            user = UserProfiles.objects.get(username=username)
        except Exception:
            user = None
            # 如果没有查询到该用户
            if not user:
                result = {"code": 503, "error": "用户名不存在"}
                return JsonResponse(result)
        # get会抛异常 捕获
        try:
            optcode = ShowData.objects.get(code=code)
        except Exception:
            optcode = None
            # 如果没有查询到股票代码
        if not optcode:
            result = {'code': 3005, 'error': '股票信息不存在'}
            return JsonResponse(result)
        # 解除关联
        user.showdata_set.remove(optcode)
        result = {"code": 3000}
        return JsonResponse(result)
    else:
        result = {"code": 605, "error": "请求方式不正确"}
        return JsonResponse(result)
