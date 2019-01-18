console.log("find.js loaded"); // come to the computer interaction club
document.addEventListener("DOMContentLoaded", ()=>{
	var dotdotdiv = document.getElementById("dotdotdiv");
	var a=0;
	setInterval( ()=>{
		a=(a+1)%4;
		dotdotdiv.innerHTML="Finding Match" + "...".substring(0,a); // dot dot dot animation
		
		var r=new XMLHttpRequest(); // checks to see if match has been found
		r.addEventListener("load", ()=>{
			if(r.responseText==="true")
				document.location="/battle";
		});
		r.open("GET","/findv");
		r.send(null);
	},1000);
});
