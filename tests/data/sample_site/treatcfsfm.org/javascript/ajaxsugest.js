// JavaScript Document
var xmlHttp
function getCaptcha()
{
	xmlHttp=GetXmlHttpObject()
	if (xmlHttp==null)
  	{
  		alert ("Browser does not support HTTP Request")
 		return
 	 } 
	 //Here xyz is passed to make the browser think that its accesing a new page
	 //Required for some browsers
	 var url="./include/getCaptcha.php?xyz="+Math.random()
	 xmlHttp.onreadystatechange=captchaChanged 
	 xmlHttp.open("GET",url,true)
	 xmlHttp.send(null)
	
}
function captchaChanged() 
{ 
	if (xmlHttp.readyState==4 || xmlHttp.readyState=="complete")
 	{  	
 		document.getElementById("divCaptcha").innerHTML=xmlHttp.responseText 
 	} 
}



function stateChanged() 
{ 
if (xmlHttp.readyState==4 || xmlHttp.readyState=="complete")
 { 
 document.getElementById("txtHint").innerHTML=xmlHttp.responseText 
 } 
}

function GetXmlHttpObject()
{
var xmlHttp=null;
try
 {
 // Firefox, Opera 8.0+, Safari
 xmlHttp=new XMLHttpRequest();
 }
catch (e)
 {
 // Internet Explorer
 try
  {
  xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
  }
 catch (e)
  {
	  
  xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
 }
return xmlHttp;
}