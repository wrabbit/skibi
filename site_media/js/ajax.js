//Plik jest uzywany przy ppotwierdzeniu przeczytania uwagi przez rodzica
var obj = false; 

function $(id){
return document.getElementById(id);
}

function ajax(obj){
if (window.XMLHttpRequest) { 
obj = new XMLHttpRequest(); 
} 
else if (window.ActiveXObject) { 
obj = new ActiveXObject("Microsoft.XMLHTTP"); 
} 
if (!obj) {
alert('Poddaję się( Nie mogę stworzynstancji obiektu XMLHTTP');
return false;
}
return obj
}

function sprawdz_dane(id)
{
var uwaga =id;
if($(id).checked){
potwierdz=1;
}
else {
potwierdz=0;
}
var obj = ajax(obj);
obj.open("GET",  "/potwierdz/"+potwierdz+"/"+uwaga+"/",true); 
obj.send(null);
}



/*
function sprawdz_login(login)
{
if (login == ""){
$("errors").innerHTML="<font face=arial size=1 color='blue'>Pole login jest wymagane.</font>";
}
var obj = ajax(obj);
obj.open("GET",  "/validate/login/"+login+"/",true); 
obj.onreadystatechange = function() {
if (obj.readyState == 4) 
{ 
if (obj.responseText=="exist"){
$("errors").innerHTML="<font face=arial size=1 color='blue'>Podany login już istnieje,proszę wybrać inny.</font>";
}
if (obj.responseText=="ok"){
$("errors").innerHTML="<font face=arial size=1 color='green'>Login jest dostępny.</font>";		 	 
}
}
}
obj.send(null);
}
*/
function filtruj_plec(plec,klasa)
{
var obj = ajax(obj);
obj.open("GET",  "/filter/"+klasa+"/"+plec+"/",true); 
obj.send(null);
}
