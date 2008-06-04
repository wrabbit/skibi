
var thumbnailviewer={
enableTitle: true, //Should "title" attribute of link be used as description?
enableAnimation: true, //Enable fading animation?
definefooter: '<div class="footerbar">CLOSE X</div>', //Define HTML for footer interface
defineLoading: '<img src="/site_media/loading.gif" /> Loading Image...', //Define HTML for "loading" div

/////////////No need to edit beyond here/////////////////////////

scrollbarwidth: 16,
opacitystring: 'filter:progid:DXImageTransform.Microsoft.alpha(opacity=10); -moz-opacity: 0.1; opacity: 0.1',
targetlinks:[], //Array to hold links with rel="thumbnail"

createthumbBox:function(){
//write out HTML for Image Thumbnail Viewer plus loading div
/*document.write('<div id="thumbBox" onClick="thumbnailviewer.closeit()"><div id="thumbImage"></div>'+this.definefooter+'</div>')*/
/*document.write('<div id="thumbLoading">'+this.defineLoading+'</div>')*/
this.thumbBox=document.getElementById("thumbBox")
this.thumbImage=document.getElementById("thumbImage") //Reference div that holds the shown image
this.thumbLoading=document.getElementById("thumbLoading") //Reference "loading" div that will be shown while image is fetched
this.standardbody=(document.compatMode=="CSS1Compat")? document.documentElement : document.body //create reference to common "body" across doctypes
},


centerDiv:function(divobj){ //Centers a div element on the page
var ie=document.all && !window.opera
var dom=document.getElementById
var scroll_top=(ie)? this.standardbody.scrollTop : window.pageYOffset
var scroll_left=(ie)? this.standardbody.scrollLeft : window.pageXOffset
var docwidth=(ie)? this.standardbody.clientWidth : window.innerWidth-this.scrollbarwidth
var docheight=(ie)? this.standardbody.clientHeight: window.innerHeight
var docheightcomplete=(this.standardbody.offsetHeight>this.standardbody.scrollHeight)? this.standardbody.offsetHeight : this.standardbody.scrollHeight //Full scroll height of document
var objwidth=divobj.offsetWidth //width of div element
var objheight=divobj.offsetHeight //height of div element
var topposition=(docheight>objheight)? scroll_top+docheight/2-objheight/2+"px" : scroll_top+10+"px" //Vertical position of div element: Either centered, or if element height larger than viewpoint height, 10px from top of viewpoint
divobj.style.left=docwidth/2-objwidth/2+"px" //Center div element horizontally
divobj.style.top=Math.floor(parseInt(topposition))+"px"
divobj.style.visibility="visible"
},

showthumbBox:function(){ //Show ThumbBox div
this.centerDiv(this.thumbBox)
if (this.enableAnimation){ //If fading animation enabled
this.currentopacity=0.1 //Starting opacity value
this.opacitytimer=setInterval("thumbnailviewer.opacityanimation()", 20)
}
},


loadimage:function(link){ //Load image function that gets attached to each link on the page with rel="thumbnail"
if (this.thumbBox.style.visibility=="visible") //if thumbox is visible on the page already
this.closeit() //Hide it first (not doing so causes triggers some positioning bug in Firefox
var imageHTML='<img src="'+link.getAttribute("href")+'" style="'+this.opacitystring+'" />' //Construct HTML for shown image
if (this.enableTitle && link.getAttribute("title")) //Use title attr of the link as description?
imageHTML+='<br />'+link.getAttribute("title")
this.centerDiv(this.thumbLoading) //Center and display "loading" div while we set up the image to be shown
this.thumbImage.innerHTML=imageHTML //Populate thumbImage div with shown image's HTML (while still hidden)
this.featureImage=this.thumbImage.getElementsByTagName("img")[0] //Reference shown image itself
this.featureImage.onload=function(){ //When target image has completely loaded
thumbnailviewer.thumbLoading.style.visibility="hidden" //Hide "loading" div
thumbnailviewer.showthumbBox() //Display "thumbbox" div to the world!
}
if (document.all && !window.createPopup) //Target IE5.0 browsers only. Address IE image cache not firing onload bug: panoramio.com/blog/onload-event/
this.featureImage.src=link.getAttribute("href")
this.featureImage.onerror=function(){ //If an error has occurred while loading the image to show
thumbnailviewer.thumbLoading.style.visibility="hidden" //Hide "loading" div, game over
}
},

setimgopacity:function(value){ //Sets the opacity of "thumbimage" div per the passed in value setting (0 to 1 and in between)
var targetobject=this.featureImage
if (targetobject.filters && targetobject.filters[0]){ //IE syntax
if (typeof targetobject.filters[0].opacity=="number") //IE6
targetobject.filters[0].opacity=value*100
else //IE 5.5
targetobject.style.filter="alpha(opacity="+value*100+")"
}
else if (typeof targetobject.style.MozOpacity!="undefined") //Old Mozilla syntax
targetobject.style.MozOpacity=value
else if (typeof targetobject.style.opacity!="undefined") //Standard opacity syntax
targetobject.style.opacity=value
else //Non of the above, stop opacity animation
this.stopanimation()
},

opacityanimation:function(){ //Gradually increase opacity function
this.setimgopacity(this.currentopacity)
this.currentopacity+=0.1
if (this.currentopacity>1)
this.stopanimation()
},

stopanimation:function(){
if (typeof this.opacitytimer!="undefined")
clearInterval(this.opacitytimer)
},


closeit:function(){ //Close "thumbbox" div function
this.stopanimation()
this.thumbBox.style.visibility="hidden"
this.thumbImage.innerHTML=""
this.thumbBox.style.left="-2000px"
this.thumbBox.style.top="-2000px"
},

cleanup:function(){ //Clean up routine on page unload
this.thumbLoading=null
if (this.featureImage) this.featureImage.onload=null
this.featureImage=null
this.thumbImage=null
for (var i=0; i<this.targetlinks.length; i++)
this.targetlinks[i].onclick=null
this.thumbBox=null
},

dotask:function(target, functionref, tasktype){ //assign a function to execute to an event handler (ie: onunload)
var tasktype=(window.addEventListener)? tasktype : "on"+tasktype
if (target.addEventListener)
target.addEventListener(tasktype, functionref, false)
else if (target.attachEvent)
target.attachEvent(tasktype, functionref)
},

init:function(){ //Initialize thumbnail viewer script by scanning page and attaching appropriate function to links with rel="thumbnail"
if (!this.enableAnimation)
this.opacitystring=""
var pagelinks=document.getElementsByTagName("a")
for (var i=0; i<pagelinks.length; i++){ //BEGIN FOR LOOP
if (pagelinks[i].getAttribute("rel") && pagelinks[i].getAttribute("rel")=="thumbnail"){ //Begin if statement
pagelinks[i].onclick=function(){
thumbnailviewer.stopanimation() //Stop any currently running fade animation on "thumbbox" div before proceeding
thumbnailviewer.loadimage(this) //Load image
return false
}
this.targetlinks[this.targetlinks.length]=pagelinks[i] //store reference to target link
} //end if statement
} //END FOR LOOP
//Reposition "thumbbox" div when page is resized
this.dotask(window, function(){if (thumbnailviewer.thumbBox.style.visibility=="visible") thumbnailviewer.centerDiv(thumbnailviewer.thumbBox)}, "resize")


} //END init() function

}

thumbnailviewer.createthumbBox() //Output HTML for the image thumbnail viewer
thumbnailviewer.dotask(window, function(){thumbnailviewer.init()}, "load") //Initialize script on page load
thumbnailviewer.dotask(window, function(){thumbnailviewer.cleanup()}, "unload")

//Style Sheet Switcher version 1.1 Oct 10th, 2006
//Author: Dynamic Drive: http://www.dynamicdrive.com
//Usage terms: http://www.dynamicdrive.com/notice.htm

var manual_or_random="manual" //"manual" or "random"
var randomsetting="3 days" //"eachtime", "sessiononly", or "x days (replace x with desired integer)". Only applicable if mode is random.

//////No need to edit beyond here//////////////

function getCookie(Name) { 
var re=new RegExp(Name+"=[^;]+", "i"); //construct RE to search for target name/value pair
if (document.cookie.match(re)) //if cookie found
return document.cookie.match(re)[0].split("=")[1] //return its value
return null
}

function setCookie(name, value, days) {
var expireDate = new Date()
//set "expstring" to either future or past date, to set or delete cookie, respectively
var expstring=(typeof days!="undefined")? expireDate.setDate(expireDate.getDate()+parseInt(days)) : expireDate.setDate(expireDate.getDate()-5)
document.cookie = name+"="+value+"; expires="+expireDate.toGMTString()+"; path=/";
}

function deleteCookie(name){
setCookie(name, "moot")
}


function setStylesheet(title, randomize){ //Main stylesheet switcher function. Second parameter if defined causes a random alternate stylesheet (including none) to be enabled
var i, cacheobj, altsheets=[""]
for(i=0; (cacheobj=document.getElementsByTagName("link")[i]); i++) {
if(cacheobj.getAttribute("rel").toLowerCase()=="alternate stylesheet" && cacheobj.getAttribute("title")) { //if this is an alternate stylesheet with title
cacheobj.disabled = true
altsheets.push(cacheobj) //store reference to alt stylesheets inside array
if(cacheobj.getAttribute("title") == title) //enable alternate stylesheet with title that matches parameter
cacheobj.disabled = false //enable chosen style sheet
}
}
if (typeof randomize!="undefined"){ //if second paramter is defined, randomly enable an alt style sheet (includes non)
var randomnumber=Math.floor(Math.random()*altsheets.length)
altsheets[randomnumber].disabled=false
}
return (typeof randomize!="undefined" && altsheets[randomnumber]!="")? altsheets[randomnumber].getAttribute("title") : "" //if in "random" mode, return "title" of randomly enabled alt stylesheet
}

function chooseStyle(styletitle, days){ //Interface function to switch style sheets plus save "title" attr of selected stylesheet to cookie
if (document.getElementById){
setStylesheet(styletitle)
setCookie("mysheet", styletitle, days)
}
}

function indicateSelected(element){ //Optional function that shows which style sheet is currently selected within group of radio buttons or select menu
if (selectedtitle!=null && (element.type==undefined || element.type=="select-one")){ //if element is a radio button or select menu
var element=(element.type=="select-one") ? element.options : element
for (var i=0; i<element.length; i++){
if (element[i].value==selectedtitle){ //if match found between form element value and cookie value
if (element[i].tagName=="OPTION") //if this is a select menu
element[i].selected=true
else //else if it's a radio button
element[i].checked=true
break
}
}
}
}

if (manual_or_random=="manual"){ //IF MANUAL MODE
var selectedtitle=getCookie("mysheet")
if (document.getElementById && selectedtitle!=null) //load user chosen style sheet from cookie if there is one stored
setStylesheet(selectedtitle)
}
else if (manual_or_random=="random"){ //IF AUTO RANDOM MODE
if (randomsetting=="eachtime")
setStylesheet("", "random")
else if (randomsetting=="sessiononly"){ //if "sessiononly" setting
if (getCookie("mysheet_s")==null) //if "mysheet_s" session cookie is empty
document.cookie="mysheet_s="+setStylesheet("", "random")+"; path=/" //activate random alt stylesheet while remembering its "title" value
else
setStylesheet(getCookie("mysheet_s")) //just activate random alt stylesheet stored in cookie
}
else if (randomsetting.search(/^[1-9]+ days/i)!=-1){ //if "x days" setting
if (getCookie("mysheet_r")==null || parseInt(getCookie("mysheet_r_days"))!=parseInt(randomsetting)){ //if "mysheet_r" cookie is empty or admin has changed number of days to persist in "x days" variable
setCookie("mysheet_r", setStylesheet("", "random"), parseInt(randomsetting)) //activate random alt stylesheet while remembering its "title" value
setCookie("mysheet_r_days", randomsetting, parseInt(randomsetting)) //Also remember the number of days to persist per the "x days" variable
}
else
setStylesheet(getCookie("mysheet_r")) //just activate random alt stylesheet stored in cookie
} 
}


var dhtmlgoodies_tooltip = false;
	var dhtmlgoodies_tooltipShadow = false;
	var dhtmlgoodies_shadowSize = 4;
	var dhtmlgoodies_tooltipMaxWidth = 200;
	var dhtmlgoodies_tooltipMinWidth = 100;
	var dhtmlgoodies_iframe = false;
	var tooltip_is_msie = (navigator.userAgent.indexOf('MSIE')>=0 && navigator.userAgent.indexOf('opera')==-1 && document.all)?true:false;
	function showTooltip(e,tooltipTxt)
	{
		
		var bodyWidth = Math.max(document.body.clientWidth,document.documentElement.clientWidth) - 20;
	
		if(!dhtmlgoodies_tooltip){
			dhtmlgoodies_tooltip = document.createElement('DIV');
			dhtmlgoodies_tooltip.id = 'dhtmlgoodies_tooltip';
			dhtmlgoodies_tooltipShadow = document.createElement('DIV');
			dhtmlgoodies_tooltipShadow.id = 'dhtmlgoodies_tooltipShadow';
			
			document.body.appendChild(dhtmlgoodies_tooltip);
			document.body.appendChild(dhtmlgoodies_tooltipShadow);	
			
			if(tooltip_is_msie){
				dhtmlgoodies_iframe = document.createElement('IFRAME');
				dhtmlgoodies_iframe.frameborder='5';
				dhtmlgoodies_iframe.style.backgroundColor='#FFFFFF';
				dhtmlgoodies_iframe.src = '#'; 	
				dhtmlgoodies_iframe.style.zIndex = 100;
				dhtmlgoodies_iframe.style.position = 'absolute';
				document.body.appendChild(dhtmlgoodies_iframe);
			}
			
		}
		
		dhtmlgoodies_tooltip.style.display='block';
		dhtmlgoodies_tooltipShadow.style.display='block';
		if(tooltip_is_msie)dhtmlgoodies_iframe.style.display='block';
		
		var st = Math.max(document.body.scrollTop,document.documentElement.scrollTop);
		if(navigator.userAgent.toLowerCase().indexOf('safari')>=0)st=0; 
		var leftPos = e.clientX + 10;
		
		dhtmlgoodies_tooltip.style.width = null;	// Reset style width if it's set 
		dhtmlgoodies_tooltip.innerHTML = tooltipTxt;
		dhtmlgoodies_tooltip.style.left = leftPos + 'px';
		dhtmlgoodies_tooltip.style.top = e.clientY + 10 + st + 'px';

		
		dhtmlgoodies_tooltipShadow.style.left =  leftPos + dhtmlgoodies_shadowSize + 'px';
		dhtmlgoodies_tooltipShadow.style.top = e.clientY + 10 + st + dhtmlgoodies_shadowSize + 'px';
		
		if(dhtmlgoodies_tooltip.offsetWidth>dhtmlgoodies_tooltipMaxWidth){	/* Exceeding max width of tooltip ? */
			dhtmlgoodies_tooltip.style.width = dhtmlgoodies_tooltipMaxWidth + 'px';
		}
		
		var tooltipWidth = dhtmlgoodies_tooltip.offsetWidth;		
		if(tooltipWidth<dhtmlgoodies_tooltipMinWidth)tooltipWidth = dhtmlgoodies_tooltipMinWidth;
		
		
		dhtmlgoodies_tooltip.style.width = tooltipWidth + 'px';
		dhtmlgoodies_tooltipShadow.style.width = dhtmlgoodies_tooltip.offsetWidth + 'px';
		dhtmlgoodies_tooltipShadow.style.height = dhtmlgoodies_tooltip.offsetHeight + 'px';		
		
		if((leftPos + tooltipWidth)>bodyWidth){
			dhtmlgoodies_tooltip.style.left = (dhtmlgoodies_tooltipShadow.style.left.replace('px','') - ((leftPos + tooltipWidth)-bodyWidth)) + 'px';
			dhtmlgoodies_tooltipShadow.style.left = (dhtmlgoodies_tooltipShadow.style.left.replace('px','') - ((leftPos + tooltipWidth)-bodyWidth) + dhtmlgoodies_shadowSize) + 'px';
		}
		
		if(tooltip_is_msie){
			dhtmlgoodies_iframe.style.left = dhtmlgoodies_tooltip.style.left;
			dhtmlgoodies_iframe.style.top = dhtmlgoodies_tooltip.style.top;
			dhtmlgoodies_iframe.style.width = dhtmlgoodies_tooltip.offsetWidth + 'px';
			dhtmlgoodies_iframe.style.height = dhtmlgoodies_tooltip.offsetHeight + 'px';
		
		}
				
	}
	
	function hideTooltip()
	{
		dhtmlgoodies_tooltip.style.display='none';
		dhtmlgoodies_tooltipShadow.style.display='none';		
		if(tooltip_is_msie)dhtmlgoodies_iframe.style.display='none';		
	}