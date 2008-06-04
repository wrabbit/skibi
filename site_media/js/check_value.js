function $(id) {
     return document.getElementById(id);
}

function checkwagi(id){

var waga=/(^([1-6]|1[0])$)/
if (waga.test($(id).value))
testresult=true
else{
$(id).value = ''
testresult=false
}
return (testresult)
}

function checkoceny(id,kolumny){
var ocena=/(^(1[+-]|2[+-]|3[+-]|4[+-]|5[+-]|1[+-]|6[-]|[1-6])$)/ 
if (ocena.test($(id).value))
testresult=true
else{
$(id).value = ''
testresult=false
}
if ($(id).value=='1' && id.indexOf('pro')!=-1){
var curleft = sprawdzLeft(kolumny);
var curtop = sprawdzTop(kolumny);
$("info").innerHTML='<img src=/site_media/images/info11.gif />';
$("info").style.left = curleft+0+'px';
$("info").style.top = curtop+-180+'px';
}
else{
$("info").innerHTML='';
}
var tab = new Array();
user = id.split("-")[1]
for (var i = 0; i < kolumny; ++i)
	if($(String(i)+"-"+user).value != '')
	    
		tab.push($(String(i)+"-"+user).value)
	var sum = 0;
    for (i=0; i<tab.length; i++)
        sum = sum + parseInt(tab[i]);
    if (tab.length > 0)
	    $('sr'+(kolumny+1)+'-'+user).value = sum / tab.length;
    else
	    $('sr'+(kolumny+1)+'-'+user).value = '';
return (testresult)
}

function checksrednie(id){

var srednia=/(^\d+$)|(^\d+\.\d+$)/
if (srednia.test($(id).value))
testresult=true
else{
$(id).value = ''
testresult=false
}
return (testresult)
}
