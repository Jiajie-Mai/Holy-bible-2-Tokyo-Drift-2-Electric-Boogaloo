console.log("find.js loaded");
document.addEventListener("DOMContentLoaded", ()=>{
	var dotdotdiv = document.getElementById("dotdotdiv");
	var a=0;
	setInterval( ()=>{
		a=(a+1)%4;
		dotdotdiv.innerHTML="Finding Match" + "...".substring(0,a);
	},10);
});
