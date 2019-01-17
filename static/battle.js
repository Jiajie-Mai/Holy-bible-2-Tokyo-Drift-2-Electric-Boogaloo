console.log("battle.js loaded");
document.addEventListener("DOMContentLoaded", () => {
	setInterval( ()=>{
		var req=new XMLHttpRequest();
		req.addEventListener("load", ()=>{
			if(req.responseText != "None"){
				console.log(req.responseText);
				var d = JSON.parse(req.responseText);
				for(var i=0;i<5;i++){
					syms[i].innerHTML = d.stocks[i][0];
					nams[i].innerHTML = d.stocks[i][1].length < 25 ? d.stocks[i][1] : d.stocks[i][1].substr(0,22) + "...";
				}
				p.innerHTML = d.p;
				pdosh.innerHTML = d.pdosh;
				e.innerHTML = d.e;
				edosh.innerHTML = d.edosh;
				round.innerHTML = d.round;
			}
		});
		req.open("GET","/minf");
		req.send(null);
	},1000);
	var move = (i)=>{
		var req = new XMLHttpRequest();
		req.open("GET","/mv");
		req.send("dir="+i); // 0 - do NOTHIGN + number is buy that stock number - number shorts
	}; // anything else is just considered a zero
	var e = document.getElementById("e");
    var edosh = document.getElementById("edosh");
    var round = document.getElementById("round");
    var stock = document.getElementById("stock");
	var p = document.getElementById("p");
    var pdosh = document.getElementById("pdosh");
	var syms = [], nams = [];
	for(var i=1;i<=5;i++){
		syms.push(document.getElementById("stoc"+i+"sym"));
		nams.push(document.getElementById("stoc"+i+"nam"));
		document.getElementById("stoc"+i+"buy").addEventListener("click", ()=>{move(i);});
		document.getElementById("stoc"+i+"sel").addEventListener("click", ()=>{move(-1*i);});
	}
});
