//---- V A L I D A T I O N    F U N T I O N  
// B - Blank , N - Number field ,  T- Text field , E- email check, P - password
function mf_validation(obj,type,msg,err_div) 
{ 
    // Blank Field Validation
	if (type=="B") 
	{ 
	  // removing white spaces
	  obj.value = trim(obj.value);
		
		if(obj.value=="") 
		{ 
			err_div.innerHTML = msg;
			obj.select();
			obj.focus(); 
			return false; 
		} 
		else
		{
				err_div.innerHTML = '';
				return true;
		}
		
	} // end if type B 
			
			
		// Number Field Validation
			if (type=="N") 
			{ 
			  // removing white spaces
 			   obj.value = trim(obj.value);
			   
				if(obj.value=="" || obj.value<0 || isNaN(obj.value)==true) 
				{ 
					err_div.innerHTML = msg;
					obj.select();
					obj.focus(); 
					return false; 
				} 
				else
				{
					 	err_div.innerHTML = '';
						return true;
				}
 
			} // end if type N
			
		
 		// Text Field Validation
			if (type=="T") 
			{ 
			  // removing white spaces
	 		   obj.value = trim(obj.value);
			   
				var last = obj.value;
				var flag = 1;
				for (var i = 0; i < last.length; i++)
				{
					var ch = last.substring(i, i + 1);
					if (((ch < "a" || "z" < ch) &&  (ch!=" " && ch!=",")) && ((ch < "64" || "Z" < ch) &&  (ch!=" " && ch!=",")))
						{
							flag = 0;
							break;
						}
				}
				if( flag==0 )
				 {
					err_div.innerHTML = msg;
					obj.select();
					obj.focus();
					return false;
				 }
				 else
				{
					 	err_div.innerHTML = '';
						return true;
				}
		   	} // end if type T 
			
			
			// Alfaneumeric validation Field Validation not allowed special characters
			if (type=="TN") 
			{ 
			  // removing white spaces
	 		   obj.value = trim(obj.value);
			   
				var flag = 1;
				
				var iChars = "*|,\":<>[]{}`\';()&$%";

			   for (var i = 0; i < obj.value.length; i++)
			    {
				  if (iChars.indexOf(obj.value.charAt(i)) != -1)
				   {
					 flag = 0;
					 break;
				   }
			    }
				
				if(isNaN(obj.value)==false)
		 		  flag = 0;
				
				if(flag==0 )
				 {
					err_div.innerHTML = msg;
					obj.select();
					obj.focus();
					return false;
				 }
				 else
				{
					 	err_div.innerHTML = '';
						return true;
				}
		   	} // end if type TN
			
			// Email Field Validation
			if (type=="E") 
			{ 
			   // removing white spaces
			    obj.value = trim(obj.value);
				
				if(emailCheck(obj.value)==false) 
				 { 
						err_div.innerHTML = msg;
						obj.select();
						obj.focus(); 
						return false; 
				 } 
				else
				 {
					 	err_div.innerHTML = '';
						return true;
			 	 }
 
			} // end if type E 
			
			
			// URL Field Validation
			if (type=="U") 
			{ 
			   // removing white spaces
			   obj.value = trim(obj.value);
			   
				if(isValidURL(obj.value)==false) 
					{ 
						err_div.innerHTML = msg; 
						obj.select();
						obj.focus(); 
						return false; 
					} 
				else
				{
					 	err_div.innerHTML = '';
						return true;
				}
 
			} // end if type U 	
			
			
			// blank image upload validation
			if (type=="I") 
			{ 
			   // removing white spaces
			   //obj.value = trim(obj.value);
			   
				if (!/(\.(gif|jpg|jpeg|png))$/i.test(obj.value))
					{ 
						err_div.innerHTML = msg;
						obj.select();
						obj.focus(); 
						return false; 
					} 
				else
				  {
					 	err_div.innerHTML = '';
						return true;
			  	 }	
 
			} // end if type I
		
				if (type=="V") 
			{ 
			   // removing white spaces
			   //obj.value = trim(obj.value);
			   
				if (!/(\.(3g2|3gp|asf|asx|avi|flv|mkv|mov|mp4|mpg|qt|rm|swf|vob|wmv|mpeg|Movie Clip))$/i.test(obj.value))
					{ 
						err_div.innerHTML = msg;
						obj.select();
						obj.focus(); 
						return false; 
					} 
				else
				  {
					 	err_div.innerHTML = '';
						return true;
			  	 }	
 
			} // end if type I
		
			
			// zip validation
			if (type=="Z") 
			{ 
			   // removing white spaces
			   obj.value = trim(obj.value);
			   
				if(obj.value.length<5 || obj.value=='00000')	 
				 {
						 err_div.innerHTML = msg;
						 obj.focus();
						 return false;
				   }

				else
				  {
					 	err_div.innerHTML = '';
						return true;
			  	 }	
 
			} // end if type I


      // FCKEditor Validation
			if (type=="FCK") 
			{ 
				var inst = FCKeditorAPI.GetInstance('contents');
				var sValue = inst.GetHTML();		
				if(sValue=='')
				{  
				    err_div.innerHTML = msg;
					return false;
				} 
				else
				{
					 	err_div.innerHTML = '';
						return true;
				}

			
			} // end if type FCK 
			
			
			
			
			 // FCKEditor Validation
			if (type=="FCK1") 
			{ 
				var inst = FCKeditorAPI.GetInstance('txtcontent');
				var sValue = inst.GetHTML();		
				if(sValue=='')
				{  
				    err_div.innerHTML = msg;
					return false;
				} 
				else
				{
					 	err_div.innerHTML = '';
						return true;
				}

			
			} // end if type FCK 
 
		 
} // END FUNCTION  



// function for phone no validation Starts *****************************************

function validate_phone(obj,msg,err_div)
{
	
var ind1=obj.value.indexOf('-');
var rm=obj.value.substring(ind1+1);
var ind2=rm.indexOf('-');
if(obj.value.length<10)
{
  err_div.innerHTML = msg;	
   obj.select();
  obj.focus();
   return false;
}
if(ind1!=3 || ind2 !=3)
{
   err_div.innerHTML = msg;	
   obj.select();
  obj.focus();
   return false;
}
if(!isNumeric(obj.value.substring(0,3)))
  {
   err_div.innerHTML = msg;	
   obj.select();
   obj.focus();
   return false;
  } 
if(!isNumeric(obj.value.substring(4,7)))
  {
   err_div.innerHTML = msg;	
   obj.select();
   obj.focus();
    return false;
  } 
if(!isNumeric(obj.value.substring(8,obj.value.length)))
  {
  err_div.innerHTML = msg;
  obj.select();
   obj.focus();
   return false;
  }  
if(parseInt(obj.value.substring(0,3))==0)
{
 err_div.innerHTML = msg;
 obj.select();
  obj.focus();
  return false; 
}
if(parseInt(obj.value.substring(4,7))==0)
{
  err_div.innerHTML = msg;
  obj.select();
   obj.focus();
   return false;
 
}
if(parseInt(obj.value.substring(8,obj.value.length))==0)
{
  err_div.innerHTML = msg;	
  obj.select();
   obj.focus();
   return false;
 
}
}
//end of validate_phone

//Time Validation
function validate_time(obj,msg,err_div)
{
	
	if(obj.start_time.value=='')	
	{
 	  err_div.innerHTML = msg;	
		obj.select();		
		obj.focus(); 
	  return false;
		 
	}
	if(obj.end_time.value=='')	
	{
 	 err_div.innerHTML = msg;	
		obj.select();		
		obj.focus(); 
	  return false;
		 
	}
	var tf =obj.start_time.value.split(':');
    var tt = obj.end_time.value.split(':');
 
	 
    var time_from = tf[0] + tf[1];
    var time_to =   tt[0] + tt[1];
	  
    if(time_from > time_to)
    {
	 err_div.innerHTML = msg;	
	 return false;
    }
}//end of time validator



function mf_phone(obj,msg, err_div) 
{ 
	
	var RegExp=/^[0-9]\d{2}-\d{3}-\d{4}$/;
	if(RegExp.test(obj.value))
	{ 
		 err_div.innerHTML = '';
         return true;
    }
	else
	{ 
		err_div.innerHTML = msg;	
		obj.select();		
		obj.focus(); 
		return false;
    }
	//if(!checkInternationalPhone(obj.value))
//	{
//		err_div.innerHTML = msg;	
//		obj.select();		
//		obj.focus(); 
//		return false; 
//	}
//	else
//	 {
//			err_div.innerHTML = '';
//			return true;
//	 }
}




/**
 * DHTML phone number validation script. Courtesy of SmartWebby.com (http://www.smartwebby.com/dhtml/)
 */

// Declaring required variables
var digits = "0123456789";
// non-digit characters which are allowed in phone numbers
var phoneNumberDelimiters = "()- ";
// characters which are allowed in international phone numbers
// (a leading + is OK)
var validWorldPhoneChars = phoneNumberDelimiters + "+";
// Minimum no of digits in an international phone no.
var minDigitsInIPhoneNumber = 10;

function isInteger(s)
{   var i;
    for (i = 0; i < s.length; i++)
    {   
        // Check that current character is number.
        var c = s.charAt(i);
        if (((c < "0") || (c > "9"))) return false;
    }
    // All characters are numbers.
    return true;
}

function stripCharsInBag(s, bag)
{   var i;
    var returnString = "";
    // Search through string's characters one by one.
    // If character is not in bag, append to returnString.
    for (i = 0; i < s.length; i++)
    {   
        // Check that current character isn't whitespace.
        var c = s.charAt(i);
        if (bag.indexOf(c) == -1) returnString += c;
    }
    return returnString;
}

function checkInternationalPhone(strPhone)
{
	s=stripCharsInBag(strPhone,validWorldPhoneChars);
	return (isInteger(s) && s.length >= minDigitsInIPhoneNumber);
}

// function for phone no validation Ends *****************************************

// function for url validation

function isValidURL(url){ 
    var RegExp = /^(([\w]+:)?\/\/)?(([\d\w]|%[a-fA-f\d]{2,2})+(:([\d\w]|%[a-fA-f\d]{2,2})+)?@)?([\d\w][-\d\w]{0,253}[\d\w]\.)+[\w]{2,4}(:[\d]+)?(\/([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)*(\?(&?([-+_~.\d\w]|%[a-fA-f\d]{2,2})=?)*)?(#([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)?$/; 
    if(RegExp.test(url)){ 
         return true;
    }else{ 
		return false;
    } 
} 


// function for email no validation
function emailCheck(str1) 
{ 
        var RegExp = /^((([a-z]|[A-Z]|[0-9]|!|#|$|%|&|'|\*|\+|\-|\/|=|\?|\^|_|`|\{|\||\}|~)+(\.([a-z]|[0-9]|!|#|$|%|&|'|\*|\+|\-|\/|=|\?|\^|_|`|\{|\||\}|~)+)*)@((((([a-z] |[A-Z] |[0-9])([a-z] |[A-Z]|[0-9]|\-){0,61}([a-z]|[A-Z]|[0-9])\.))*([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9]|\-){0,61}([a-z]|[A-Z]|[0-9])\.)[\w]{2,4}|(((([0-9]){1,3}\.){3}([0-9]){1,3}))|(\[((([0-9]){1,3}\.){3}([0-9]){1,3})\])))$/ 
	
    if(RegExp.test(str1)){ 
        return true;
    }else{ 
		return false;
    } 


}//end of function emailCheck


// audio / video file handelling
function videoPopup(url,type)
 {
 
 var media;
 if(type==1)
  media = "audio";
 else 
   media = "video";
 if(url=="#")
  alert("Sorry "+ media + " is not available");
 else
    window.open(url,'popup','width=620,height=450,top=100,left=220,resizable=0,scrollbars=1');   
 }


//  function for enter key form submission

function checkEnter(e,form)
{ 

	//e is event object passed from function invocation
	var characterCode;  //literal character code will be stored in this variable
	
	if(e && e.which)
	{
	 //if which property of event object is supported (NN4)
		e = e
		characterCode = e.which //character code is contained in NN4's which property
	}
	else
	{
		e = event
		characterCode = e.keyCode //character code is contained in IE's keyCode property
	}
	
	if(characterCode == 13)
	{ //if generated character code is equal to ascii 13 (if enter key)
		form.submit() //submit the form
		return false
	}
	else
	{
		return true
	}

}


// JavaScript Document

function click_validation(e)
{
//	 alert('sdfs');
	//alert(event.button + navigator.appName  );
  if (navigator.appName == 'Netscape'
           && e.which == 3)
     {
      alert("Right Click is not allowded")
      return false;
      }
   else 
    {
      if (navigator.appName == 'Microsoft Internet Explorer'
          && event.button==2)
	   {
       alert("Right Click is not allowded")
		return false;
       }
   return true;
    }
}



// password Validation function
function checkPassword(objPass,objCpass,objUid)
 {
		var strPass = objPass.value;
		var strCpass = objCpass.value;
		var strUid = objUid.value;	
		
		
		var len1=strPass.length;
		var len2=strCpass.length;
		
		if(len1 < 6)
		{
		alert('password should be of atleast 6 characters');
		objPass.value="";
		objCpass.value="";
		objPass.focus();
		return false;
		}
		
		if(strUid == strPass)
		{
		alert('Password and UserID should not same');
		objPass.value="";
		objCpass.value="";
		objPass.focus();
		return false;
		}
		
		
		if(len1!=len2)
		{
		alert('confirm password not match');
		objCpass.value="";
		 objCpass.focus();
		return false;
		}
		
		if(strPass != strCpass)
		{
		alert('confirm password not match');
		objCpass.value="";
		objCpass.focus();
		return false;
		}	 

 }
 
 // password Validation
	
	
// trim functions
function trim(stringToTrim) {
	return stringToTrim.replace(/^\s+|\s+$/g,"");
}
function ltrim(stringToTrim) {
	return stringToTrim.replace(/^\s+/,"");
}
function rtrim(stringToTrim) {
	return stringToTrim.replace(/\s+$/,"");
}


// function for add to favourites
function favit(heading,address)
 {
	if(window.sidebar)
	  {
		  window.sidebar.addPanel(document.title,location.href,''); // for mozilla, netscape
	  }
	 else
	  { 
		  window.external.AddFavorite(location.href,document.title); // for IE
	  }
 }
 
/* 
 
*/
// select all check boxes
function Checkall(form)
 { 
   for (var i = 0; i < form.elements.length; i++)
     {    
	  if(form.elements[i].disabled!=true)
	   { 
	     flag=1;
         eval("form.elements[" + i + "].checked = form.elements[0].checked");  
	   }
     } 
 } 
 
 
 // date validations
 function chk_year(obj,msg)
{
	var current_date = new Date();
    var current_year = current_date.getFullYear();
	var dt=obj.value;
    var arr=dt.split('/');
	if(arr[2] < current_year)
	{
		alert(msg);
		return false;
	}
	else 
		return true;
	

}
function chk_mon(obj,msg)
{
	var current_date = new Date();
    // getMonth() returns 0 to 11 for months	
    var current_mon = current_date.getMonth();
	var dt=obj.value;
    var arr=dt.split('/');
	if(arr[1] < (current_mon+1))
	{
		alert(msg);
	    return false;
	}
	else
	{
			return true;
	}

}

function chk_day(obj,msg)
{
	var current_date = new Date();
    var current_day = current_date.getDate();
    var dt=obj.value;
    var arr=dt.split('/');

	if(arr[0] < current_day)
	{
		alert(msg);
	    return false;
	}
	else
		return true;
}


function validTextFile(obj,msg,err_div)
 {

// blank image upload validation
			if (!/(\.(pdf))$/i.test(obj.value))
					{ 
						err_div.innerHTML = msg;
						obj.select();
						obj.focus(); 
						return false; 
					} 
 
 }
 
 // resrincting text area characters limit
 
function chopText(elem, limit)
 {
	if(elem.value.length>=limit)
	 {
	//  alert("General information required upto 350 characters..."); 
	  elem.value=elem.value.substring(0,limit);
	 }	
	//document.frmupdateuser.cLeft.value=limit-elem.value.length;
 }
 
 
 
 // image validation function
 //image validation function
 var extArray = new Array(".jpg",".jpeg",".gif", ".png");

function image_validation(name1)
{
var file=name1;
var a=name1.split(".");
if(a[1]==undefined)
{
alert("Please upload proper photo.");
return false;
}
allowSubmit = false;
if (!file) return;
while (file.indexOf("\\") != -1)
file = file.slice(file.indexOf("\\") + 1);
ext = file.slice(file.indexOf(".")).toLowerCase();
for (var i = 0; i < extArray.length; i++) {
if (extArray[i] == ext) { allowSubmit = true; break; }
}
if (allowSubmit){}
else
{
alert("Please only upload files that end in types:  "
    + (extArray.join("  ")) + "\nPlease select a new "
    + "file to upload and submit again.");
    return false;
    }
	
}

// function for validating multiple emails
function multiEmail(obj, msg)
{
	var emails = trim(obj.value);
	var email  = emails.split(',');
	var retVal;
	for (var i = 0; i < email.length; i++)
	 {
	   email_add = trim(email[i]);	  
	   if(emailCheck(email_add) == false) 
		{ 
			alert(msg + ', Check email id ' + (i + 1)); 
			obj.select();
			obj.focus(); 
			return false; 
			break;
		} 	

     }
	
}

// function for avoiding bots to track emails
function botsMail(name, domain)
 {
	if(name!='' && domain!='') 
	 {
		var char = '@';
		document.write ("<a href=\"mailto:" + name + char + domain + "\"> Send eMail </a>");
	 }
 }
 
 function keyRestrict(e, validchars)
{
		
     var key='', keychar='';
     key = getKeyCode(e);
     if (key == null) return true;
     keychar = String.fromCharCode(key);
     keychar = keychar.toLowerCase();
     validchars = validchars.toLowerCase();
     if (validchars.indexOf(keychar) != -1)
      return true;
     if ( key==null || key==0 || key==8 || key==9 || key==13 || key==27 )
      return true;
     return false;
}
function getKeyCode(e)
{
        if (window.event)
        return window.event.keyCode;
        else if (e)
        return e.which;
        else
        return null;
}

function ismaxlength(obj)
{
    
    var mlength=obj.getAttribute? parseInt("300") : ""
    if (obj.getAttribute && obj.value.length>mlength)
    obj.value=obj.value.substring(0,mlength)
}



