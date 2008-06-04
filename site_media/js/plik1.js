
function calendar(akcja,obj,l,t)
{
var curleft = sprawdzLeft(obj);
var curtop = sprawdzTop(obj);
if(akcja!='close'){
document.getElementById("okienko3").style.display = 'block';
document.getElementById('okienko3').style.left = curleft+l+'px';
document.getElementById('okienko3').style.top = curtop+t+'px';
}
else{
document.getElementById("okienko3").style.display = 'none';
}
}

function sprawdzLeft(obj){
	var curleft = 0;
	if (obj.offsetParent){
		while (obj.offsetParent){
			curleft += obj.offsetLeft
			obj = obj.offsetParent;
		}
	}
	else if (obj.x){
		curleft += obj.x;
	}
	return curleft;
}
function sprawdzTop(obj){
	var curtop = 0;
	if (obj.offsetParent)
	{
		while (obj.offsetParent)
		{
			curtop += obj.offsetTop
			obj = obj.offsetParent;
		}
	}
	else if (obj.y){
		curtop += obj.y;
	}
	return curtop;
}
function submitForm(l)
{
document.getElementById("lg").value=l;
document.lang.submit();
}
/*EventCalendarFunctionsJavaScript */
    function changeEvent(button, rowid) {
        var formObj = button.form;
        var nameObj = formObj.elements.namedItem("name" + rowid);
        var whenObj = formObj.elements.namedItem("when" + rowid);
        var descObj = formObj.elements.namedItem("desc" + rowid);
        var rmObj   = formObj.elements.namedItem("rmbutt" + rowid);

        if (button.value == "Change")
        {
            /* enable fields, change background color, etc for update */
            nameObj.readOnly = false;
            whenObj.readOnly = false;
            descObj.readOnly = false;

            nameObj.style.background = "#FF6A6A";
            whenObj.style.background = "#FF6A6A";
            descObj.style.background = "#FF6A6A";

            if (rmObj.value != "Remove") {
                rmObj.value = "Remove";
                rmObj.style.background = "";
            }
            button.style.background = "#FF6A6A";
            button.value = "Save Changes";

            return false;
        }
        else
        {
            /* clear files for database update */
            formObj.elements.namedItem("rowid").value = "";
            formObj.elements.namedItem("name").value = "";
            formObj.elements.namedItem("when").value = "";
            formObj.elements.namedItem("desc").value = "";

            /* submit changes */
            formObj.elements.namedItem("rowid").value = rowid;
            formObj.elements.namedItem("name").value = nameObj.value;
            formObj.elements.namedItem("when").value = whenObj.value;
            formObj.elements.namedItem("desc").value = descObj.value;
            formObj.action += "upd/";
            formObj.submit();
            return true;
        }
    }

    function deleteEvent(button, rowid) {
        var formObj = button.form;
        var nameObj = formObj.elements.namedItem("name" + rowid);
        var whenObj = formObj.elements.namedItem("when" + rowid);
        var descObj = formObj.elements.namedItem("desc" + rowid);
        var chgObj   = formObj.elements.namedItem("chgbutt" + rowid);

        if (button.value == "Remove")
        {
            nameObj.style.background = "#FF6A00";
            whenObj.style.background = "#FF6A00";
            descObj.style.background = "#FF6A00";

            if (chgObj.value != "Change") {
                chgObj.value = "Change"
                chgObj.style.background = "";
            }
            button.style.background = "#FF6A00";
            button.value = "Confirm Delete";

            return false;
        }
        else
        {
            /* submit removal request */
            formObj.elements.namedItem("rowid").value = "";
            formObj.elements.namedItem("rowid").value = rowid;
            formObj.action += "del/";
            formObj.submit();
        }
        return true;
    }

    function addEvent(button) {
        var formObj = button.form;
        var nameObj = formObj.elements.namedItem("new_name");
        var whenObj = formObj.elements.namedItem("new_when");
        var descObj = formObj.elements.namedItem("new_desc");
        var dayObj  = formObj.elements.namedItem("new_day");

        /* reset fields */
        formObj.elements.namedItem("name").value = "";
        formObj.elements.namedItem("when").value = "";
        formObj.elements.namedItem("desc").value = "";

        /* submit add request (when there are things to add) */
        if (nameObj.value != "" && whenObj.value != "") {
            formObj.elements.namedItem("rowid").value = 0;
            formObj.elements.namedItem("name").value = nameObj.value;
            formObj.elements.namedItem("when").value = whenObj.value;
            formObj.elements.namedItem("desc").value = descObj.value;
            formObj.elements.namedItem("day").value = dayObj.value;
            formObj.action += "add/";
            formObj.submit();
            return true;
        }
        return false;
    }