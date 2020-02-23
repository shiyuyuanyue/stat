    var x1= 0
	var y1 = 200
	var x2 = 0
	setInterval("run()",100);
	function run(){
	x2 +=  10
	y2 = parseInt(18-Math.random()*36);
	y2 += y1
	var c=document.getElementById("myCanvas");
	var cxt=c.getContext("2d");
	cxt.strokeStyle = '#00a4ff';
	cxt.moveTo(x1,y1);
	cxt.lineTo(x2,y2);
	var y3 = y2-y1
	if(y3>14||y3< -14){
		cxt.font = "12px 微软黑体";
		cxt.fillStyle = "#00a4ff";
		var y4 = y2+y3*2+8*(y3/Math.abs(y3))
		var y5 = 120-y4/3.1415926
		var y6 = y5.toFixed(2)
		cxt.fillText(y6+'¥', x2, y4);
		cxt.textAlign = "center";
		cxt.textBaseline = "middle";
		cxt.moveTo(x2,y2);
		cxt.lineTo(x2,y2+y3*2);
	}
	x1 = x2;
	y1 = y2;
	cxt.stroke();
	 }