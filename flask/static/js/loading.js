//加载提示
var c=0;
function loading(){
    c++
    var html = '努力数据分析中...<span>' + c + '</span>秒'
    $('#loading').html(html)
}
setInterval("loading()","1000");