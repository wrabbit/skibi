#!/usr/bin/python
# Diamanda Application Set
# Boxcomments - global comment system

from random import choice
import Image, ImageDraw, ImageFont, sha
from stripogram import html2safehtml

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django import newforms as forms
from django.utils.translation import ugettext as _
from django.core.mail import mail_admins

from boxcomments.models import *
from e_dziennik.models import Aktualnosci
from django.views.generic.list_detail import object_list



class CommentForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
	title_com = forms.CharField(max_length=30)
	imgtext = forms.CharField()
	imghash = forms.CharField(widget=forms.HiddenInput)
	def clean(self):
		SALT = settings.SECRET_KEY[:20]
		if not 'imgtext' in self.cleaned_data or not self.cleaned_data['imghash'] == sha.new(SALT+self.cleaned_data['imgtext'].upper()).hexdigest():
			raise forms.ValidationError('Captha Error')
		return self.cleaned_data

def comments(request, apptype, appid, quoteid=False,add=False,page=None,header='Komentarze',):
        
	"""
	Show and add comments to defined object
	
	*apptype - application
	*appid - ID of an app record
	"""
	# create a 5 char random strin and sha hash it
	imgtext = ''.join([choice('QWERTYUOPASDFGHJKLZXCVBNM') for i in range(5)])
	SALT = settings.SECRET_KEY[:20]
	imghash = sha.new(SALT+imgtext).hexdigest()
	# create an image with the string
	im=Image.open(settings.MEDIA_ROOT + '/bg.jpg')
	draw=ImageDraw.Draw(im)
	font=ImageFont.truetype(settings.MEDIA_ROOT + '/SHERWOOD.TTF', 26)
	draw.text((5,5),imgtext, font=font, fill=(100,100,50))
	im.save(settings.MEDIA_ROOT + '/captcha/' + str(request.user) + '.jpg',"JPEG")
	
	com = Comment.objects.filter(apptype= apptype, appid = appid).order_by('-date')
	
	if len(com)>=3 and com[0].ip == com[1].ip and com[0].ip == request.META['REMOTE_ADDR']:
		ban = True
	else:
		ban = False
	try:
		if apptype == '1':
			a = Aktualnosci.objects.get(id = appid)
			title_text = a.news_title
		
	except:
		return render_to_response('bug.html', {'bug': _('No such entry')}, context_instance=RequestContext(request))
        
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			text = html2safehtml(data['text'] ,valid_tags=())
			co = Comment(title_text = title_text,title_com=data['title_com'],appid = appid, text = text, author = str(request.user.get_full_name()), ip = request.META['REMOTE_ADDR'], apptype = apptype)
			co.save()
			#mail_admins('Komentarz Dodany', 'Dodano komentarz: http://www.' + settings.SITE_KEY, fail_silently=True)
			return HttpResponseRedirect('/com/' + str(appid) + '/' + str(apptype) + '/')
		else:
			if str(form.errors).find('Captha Error') >= 0:
				if not 'imgtext' in form.errors:
					form.errors['imgtext'] = []
				form.errors['imgtext'].append(_('Captcha Error'))
			return render_to_response(
				'boxcomments/comments.html',
				{'hash': imghash,'header':'Dodaj komentarz','add':add, 'form': form, 'com': com, 'appid': appid, 'apptype': apptype, 'a': a, 'ban': ban, 'title':title_text},
				context_instance=RequestContext(request))

	if quoteid:
                #return HttpResponse(str(quoteid))
		q = Comment.objects.get(id=quoteid)
		#return HttpResponse(str(q.author))
		form =  CommentForm({'text':'[quote][b]@' + q.author + '[/b]\n' + q.text + '[/quote]\n\n'})
	else:
		form =  CommentForm()
	
        return object_list(request,
                           queryset=com,
                           paginate_by = 5,
                           page = page,
                           extra_context={'hash': imghash,'header':header,'add':add,'form': form, 'com': com, 'appid': appid, 'apptype': apptype, 'a': a, 'ban': ban, 'title':title_text},
                           template_name = 'boxcomments/comments.html')
