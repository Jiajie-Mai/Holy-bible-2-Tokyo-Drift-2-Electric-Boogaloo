
console.log("battle.js loaded");
document.addEventListener("DOMContentLoaded", () => {
	setInterval( ()=>{
		var req=new XMLHttpRequest();
		req.addEventListener("load", ()=>{
			if(req.responseText != "None"){
				var d = JSON.parse(req.responseText);
				if(d.round == 0){
					if(d.pdosh > d.edosh)
						document.location = "/win";
					else if (d.pdosh < d.edosh)
						document.location = "/loss";
					else
						document.location = "/tie";
				}
				for(var i=0;i<5;i++){
					syms[i].innerHTML = d.stocks[i][0];
					nams[i].innerHTML = d.stocks[i][1].length < 30 ? d.stocks[i][1] : d.stocks[i][1].substr(0,27) + "...";
				}
				p.innerHTML = d.p;
				pdosh.innerHTML = parseInt(d.pdosh)/100;
				e.innerHTML = d.e;
				edosh.innerHTML = parseInt(d.edosh)/100;
				round.innerHTML = d.round;
			}
		});
		req.open("GET","/minf");
		req.send(null);
	},2000);
	var move = (i)=>{
		console.log(i)
		var req = new XMLHttpRequest();
		req.open("GET","/mv?dir="+i);
		req.send(null); // 0 - do NOTHIGN + number is buy that stock number - number shorts
	}; // anything else is just considered a zero
	var e = document.getElementById("e");
    var edosh = document.getElementById("edosh");
    var round = document.getElementById("round");
    var stock = document.getElementById("stock");
	var p = document.getElementById("p");
    var pdosh = document.getElementById("pdosh");
	var syms = [], nams = [];
	for(let j=1;j<=5;j++){
		let i = j; // javascript scope is whack
		syms.push(document.getElementById("stoc"+i+"sym"));
		nams.push(document.getElementById("stoc"+i+"nam"));
		document.getElementById("stoc"+i+"buy").addEventListener("click", ()=>{move(i);});
		document.getElementById("stoc"+i+"sel").addEventListener("click", ()=>{move(-1*i);});
	}
});
