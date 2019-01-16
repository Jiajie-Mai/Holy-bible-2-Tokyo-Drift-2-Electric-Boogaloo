console.log("find.js loaded");
document.addEventListener("DOMContentLoaded", ()=>{
	var dotdotdiv = document.getElementById("dotdotdiv");
	var a=0;
	setInterval( ()=>{
		a=(a+1)%4;
		dotdotdiv.innerHTML="Finding Match" + "...".substring(0,a);
		
		var r=new XMLHttpRequest();
		r.addEventListener("load", ()=>{
			console.log(r);
			if(r.responseText==="true")
				document.location="/battle";
		});
		r.open("GET","/findv");
		r.send(null);
	},1000);
});
