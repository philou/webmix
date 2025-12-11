// JavaScript Document
function over()
{
 document.getElementById('holder').style.display="";
if(document.getElementById('divid')==null){

   
    var x=findPosX(document.getElementById('holder'));
    x=x+40;
    var y=findPosY(document.getElementById('holder'));
    y=y-113;
	var _d=document.createElement('DIV');
	_d.style.backgroundColor="white";
	_d.style.position="absolute";
	//_d.style.height="100%";
	_d.style.width="400px";
	_d.style.top=y+"px";
      _d.style.left=x+"px";
      _d.id="divid";
	  _d.style.borderWidth="1px";
	  _d.style.borderStyle="solid";
	  _d.style.borderColor="#D2D2D2";
	  _d.style.padding="5px";



 
 
 var _a=document.createElement('DIV');
_a.style.textAlign="right";
_a.innerHTML="<img src='images/close.png' alt='close' width='12' height='12' border='0'  onclick='out();' style='cursor:pointer;' />";

var _b=document.createElement('DIV');
_b.className="copy_contain1";
_b.style.paddingTop="3px";
_b.innerHTML="Permission is granted to copy or quote from this site <a href='http://www.TreatCFSFM.org' target='_blank'>(www.TreatCFSFM.org)</a> for non-commercial purposes only, provided the intended meaning is preserved, the source is identified as Treating Chronic Fatigue Syndrome and Fibromyalgia, the author is identified (if applicable), and the website URL is provided.";


 _d.style.display="";
 
 _d.appendChild(_a);
 _d.appendChild(_b);
 
 
// var anode= document.createAttribute("onmouseout");
//anode.value="out()";
//_d.setAttributeNode(anode);

    document.getElementById('holder').appendChild(_d);
	
   }

}
function out()
{

document.getElementById('holder').style.display="none";

}

function findPosX(obj)
  {
    var curleft = 0;
    if(obj.offsetParent)
        while(1) 
        {
          curleft += obj.offsetLeft;
          if(!obj.offsetParent)
            break;
          obj = obj.offsetParent;
        }
    else if(obj.x)
        curleft += obj.x;
    return curleft;
  }

  function findPosY(obj)
  {
    var curtop = 0;
    if(obj.offsetParent)
        while(1)
        {
          curtop += obj.offsetTop;
          if(!obj.offsetParent)
            break;
          obj = obj.offsetParent;
        }
    else if(obj.y)
        curtop += obj.y;
    return curtop;
  }
