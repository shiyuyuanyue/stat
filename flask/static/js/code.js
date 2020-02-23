var url = document.location.toString()
var s_url = url.split('//')
var s_url_str = s_url[1].split('/')
var code = s_url_str[1]
document.title = code + '_STAT搜索' //动态title
var username = window.localStorage.getItem('st_user')
var token = window.localStorage.getItem('st_token')

//发起搜索
$('#get_stock_code').val(code)
var get_url = 'http://127.0.0.1:8000/v1/search_api?code=' + code
    $.ajax({
        type:'get',
        url:get_url,
        dataType:'json',
        success:function(data){
            if(data.code == 3000){
                var html = ''
                html += '<div id="tt">' + data.data.title + '(' + data.data.code + ')' + '<span>最后更新:' + data.data.date +'</span><div id="time"><img src="/static/img/time.png"></div></div>'
                html += '<div id="dt"><span>综合评分</span><br>' + data.data.score + '分</div>'
                html += '<div id="dt"><span>购买欲</span><br>' + data.data.desire_buy + '</div>'
                html += '<div id="dt"><span>击败</span><br>' + data.data.beat + '%</div>'
                html += '<div id="dt"><span>搜索量</span><br>' + data.data.lkc + '次</div>'
                html += '<div id="dt"><span>历史最高</span><br>' + data.data.highest + '元</div>'
                html += '<div id="dt"><span>历史最低</span><br>' + data.data.lowest + '元</div>'
                html += '<div id="dt"><span>历史均价</span><br>' + data.data.average + '元</div>'
                html += '<div id="dt"><span>最高连涨</span><br>' + data.data.days + '天，'  + data.data.day_count + '次' + '</div>'
                html += '<div id="dt"><span>关注</span><br>' + data.data.hot + '人</div>'
                html += '<div id="dt"><span>累计追踪</span><br>' + data.data.tt + '次</div>'
                html += '<div id="dt"><span>上涨概率</span><br>' + data.data.rp + '%</div>'
                html += '<div id="dt"><span>下跌概率</span><br>' + data.data.fp + '%</div>'
                html += '<div id="dt"><span>线性回归预测</span><br>' + data.data.linear_regression + '元</div>'
                html += '<div id="dt"><span>岭回归预测</span><br>' + data.data.ridge_regression + '元</div>'
                html += '<div id="dt"><span>多项式预测</span><br>' + data.data.polynomial_regression + '元</div>'
                html += '<div id="dt"><span>AI智能预测</span><br>' + data.data.ai_prediction + '元</div>'

                html += '<div id="dt_01"><span>男女比例</span><br>' + data.data.prosex + '</div>'
                html += '<div id="dt_01"><span>年龄比例</span><br>' + data.data.proage + '</div>'
                html += '<div id="dt_01"><span>收入比例</span><br>' + data.data.proinc + '</div>'
                html += '<div id="dt_01"><span>经验比例</span><br>' + data.data.proexp + '</div>'
                html += '<div id="dt_01"><span>杠杆比例</span><br>' + data.data.prolev + '</div>'
                html += '<div id="dt_01"><span>偏好比例</span><br>' + data.data.propre + '</div>'
                html += '<div id="dt_01"><span>职业比例</span><br>' + data.data.proocc + '</div>'
                html += '<div id="dt_bt" onclick="add_code()" title="' + data.data.code + '"> +加入自选股</div>'
                var str_tup = data.data.nlp.split('/')
                var idf_str = str_tup[0]
                var rank_str = str_tup[1]

                var idf_rep = idf_str.replace(/\,/g, "</span><span>")
                var idf_01 = '<span>' + idf_rep + '</span>'
                var idf_02 =  idf_01.replace(/\(/g,"<h3>")
                var idf_03 = idf_02.replace(/\)/g,"</h3>")

                var rank_rep = rank_str.replace(/\,/g, "</span><span>")
                var rank_01 = '<span>' + rank_rep + '</span>'
                var rank_02 =  rank_01.replace(/\(/g,"<h3>")
                var rank_03 = rank_02.replace(/\)/g,"</h3>")

                console.log(rank_03)

                html += '<div id="nlp"><span>TF-IDF关键词：</span>' + idf_03 + '</div>'
                html += '<div id="nlp"><span>Text-Rank关键词：</span>' + rank_03 + '</div>'
                $('#showdatas').html(html)
            }else{
                $('#showdatas').html(code + data.error)
            }
        }

    })
//添加自选股

function add_code(code){
    var code = $('#dt_bt').attr('title')
    $.ajax({
        type:'post',
        url:'http://127.0.0.1:8000/v1/search_api',
        data:JSON.stringify({"username":username,"code":code}),
        dataType:'json',
        beforeSend: function(request) {
           request.setRequestHeader("Authorization", token)
       },
        success:function(data){
            if(data.code == 3000){
                alert(code + '添加成功，请前往个人中心查看')
                location.reload()
            }else{
                alert(data.error)
            }
        }
    })
}


//右侧内容
$.ajax({
    type:'get',
    url:'http://127.0.0.1:8000/v1/search_api',
    dataType:'json',
    success:function(data){
        if(data.code == 200){
            var html_score = ''
            var html_buy = ''
            var html_days = ''

            for (var i=0;i<data.data[0].length;i++){
                var socre_num = data.data[0][i].num
                var score_code = data.data[0][i].code
                var score_title = data.data[0][i].title
                var score_score = data.data[0][i].score

                var buy_num = data.data[1][i].num
                var buy_code = data.data[1][i].code
                var buy_title = data.data[1][i].title
                var buy_score = data.data[1][i].score

                var days_num = data.data[2][i].num
                var days_code = data.data[2][i].code
                var days_title = data.data[2][i].title
                var days_score = data.data[2][i].score

                html_score += '<li><h3>' + socre_num + '.</h3><span>' + score_score + '</span><a href="http://127.0.0.1:5000/search/' + score_code + '">' + score_title  + '</a> &nbsp;&nbsp;('+ score_code + ')</li>'
                html_buy += '<li><h3>' + buy_num + '.</h3><span>' + buy_score + '</span><a href="http://127.0.0.1:5000/search/' + buy_code + '">' + buy_title  + '</a> &nbsp;&nbsp;('+ buy_code + ')</li>'
                html_days += '<li><h3>' + days_num + '.</h3><span>' + days_score + '天</span><a href="http://127.0.0.1:5000/search/' + days_code + '">' + days_title  + '</a> &nbsp;&nbsp;('+ days_code +')</li>'
            }
            $('#article_01').html(html_score)
            $('#article_02').html(html_buy)
            $('#article_03').html(html_days)
        }else{
            alert(data.error)
        }
    }
})


//顶部状态栏

var html = ''
    if(username){
        html += '<li><a href="/">STAT首页</a></li><li><a href="/lab">实验室</a></li> '
        html += '<li><a href="#" onclick=logout()>退出</a></li>'
        html += '<li><span><a href="/home/' + username +'">' + username +'</a></span></li>'
        $('#guide_right').html(html)
    }else{
        html += '<li><a href="/login">登陆</a></li> <li><a href="/register">注册</a></li> <li><a href="/">STAT首页</a></li><li><a href="/lab">实验室</a></li>'
        $('#guide_right').html(html)
    }


//搜索框提示
$('#get_stock_code').on('input',function(){
var input_data = $(this).val()
    $.ajax({
    type:'get',
    url:'http://127.0.0.1:8000/v1/search_api?kw=' + input_data,
    dataType:'json',
    success:function(data){
        if(data.code == 3000){
            var likewords = data.data.likewords
            var html = '<div id="showwords">'
            for (var i=0;i<likewords.length;i++){
                code = likewords[i][0]
                title = likewords[i][1]
                html += '<li><a href="http://127.0.0.1:5000/' + code + '">' + code + title + '</a></li>'
            }
            html += '</div>'
            $('#show').html(html)
        }else{
            $('#show').html('<div id="showwords">'+ data.error + '</div>')
        }
    }
    })
    })

//失去焦点收起
$('#get_stock_code').blur(
   function(){
     setTimeout(
        function(){
        $('#showwords').slideUp()
    },200
    )
   }
)
//搜索
function search(){
        var input_data = $('#get_stock_code').val()
        window.location.href="http://127.0.0.1:5000/" + input_data

}
//回车搜索
$(document).keyup(function(event){
 if(event.keyCode ==13){
  search()
 }
})

//退出
function logout(){
   window.localStorage.clear()
   location.reload()
}