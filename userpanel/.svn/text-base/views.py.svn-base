#!/usr/bin/python
# Diamanda Application Set
# User Panel

from stripogram import html2safehtml
from random import choice
import Image, ImageDraw, ImageFont, sha

from django.shortcuts import render_to_response
from django import oldforms as forms
from django.core import validators
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from userpanel.models import *


def user_panel(request):
	"""
	main user panel
	"""
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/user/login/")
	return render_to_response('userpanel/panel.html', context_instance=RequestContext(request))

def userlist(request):
	"""
	list all users
	"""
	users = User.objects.all()
	return object_list(request, users, paginate_by = 25, allow_empty = True, template_name = 'userpanel/userlist.html')




class RegisterForm(forms.Manipulator):
	"""
	User registration manipulator
	"""
	def __init__(self):
		self.fields = (forms.TextField(field_name="login", length=20, max_length=200, is_required=True, validator_list=[validators.isAlphaNumeric, self.size3, self.freelogin]),
		forms.PasswordField(field_name="password1", length=20, max_length=200, is_required=True, validator_list=[validators.isAlphaNumeric, self.size4, self.equal]),
		forms.PasswordField(field_name="password2", length=20, max_length=200, is_required=True, validator_list=[validators.isAlphaNumeric, self.size4]),
		forms.TextField(field_name="imgtext", is_required=True, validator_list=[self.hashcheck], length=20),
		forms.TextField(field_name="imghash", is_required=True, length=20),
		forms.EmailField(field_name="email", is_required=True, length=20, validator_list=[self.freemail]),)
	def hashcheck(self, field_data, all_data):
		SALT = settings.SECRET_KEY[:20]
		if not all_data['imghash'] == sha.new(unicode(SALT)+unicode(field_data.upper())).hexdigest():
			raise validators.ValidationError(_("Captcha Error."))
	def size3(self, field_data, all_data):
		if len(field_data) < 4:
			raise validators.ValidationError(_("Login to short"))
	def size4(self, field_data, all_data):
		if len(field_data) < 5:
			raise validators.ValidationError(_("Password to short"))
	def equal(self, field_data, all_data):
		if all_data['password2'] != field_data:
			raise validators.ValidationError(_("Passwords do not match"))
	def freelogin(self, field_data, all_data):
		try:
			User.objects.get(username=field_data)
		except:
			pass
		else:
			raise validators.ValidationError(_("Login already taken"))
	def freemail(self, field_data, all_data):
		try:
			User.objects.get(email=field_data)
		except:
			pass
		else:
			raise validators.ValidationError(_('Email already taken'))

def register(request):
	"""
	User registration
	"""
	# create a 5 char random strin and sha hash it
	imgtext = ''.join([choice('QWERTYUOPASDFGHJKLZXCVBNM') for i in range(5)])
	SALT = settings.SECRET_KEY[:20]
	imghash = sha.new(unicode(SALT)+unicode(imgtext)).hexdigest()
	# create an image with the string
	im=Image.open(settings.MEDIA_ROOT + '/bg.jpg')
	draw=ImageDraw.Draw(im)
	font=ImageFont.truetype(settings.MEDIA_ROOT + '/SHERWOOD.TTF', 26)
	draw.text((5,5),imgtext, font=font, fill=(100,100,50))
	im.save(settings.MEDIA_ROOT + '/captcha/' + str(request.user) + '.jpg',"JPEG")
	
	manipulator = RegisterForm()
	if request.POST:
		data = request.POST.copy()
		
		errors = manipulator.get_validation_errors(data)
		if not errors:
			data['email'] = html2safehtml(data['email'] ,valid_tags=())
			try:
				user = User.objects.create_user(data['login'], data['email'], data['password1'])
			except Exception:
				data['imgtext'] = ''
				form = forms.FormWrapper(manipulator, data, errors)
				return render_to_response(
					'userpanel/register.html',
					{'error': True, 'form': form},
					context_instance=RequestContext(request))
			else:
				user.save()
				user = authenticate(username=data['login'], password=data['password1'])
				if user is not None:
					login(request, user)
				return HttpResponseRedirect("/user/")
		else:
			data['imgtext'] = ''
			form = forms.FormWrapper(manipulator, data, errors)
			return render_to_response(
				'userpanel/register.html',
				{'error': True, 'hash': imghash, 'form': form},
				context_instance=RequestContext(request))
	else:
		errors = data = {}
	form = forms.FormWrapper(manipulator, data, errors)
	return render_to_response(
		'userpanel/register.html',
		{'hash': imghash, 'form': form},
		context_instance=RequestContext(request))




class LoginForm(forms.Manipulator):
	"""
	User login manipulator
	"""
	def __init__(self):
		self.fields = (forms.TextField(field_name="login", length=30, max_length=200, is_required=True),
		forms.PasswordField(field_name="password", length=30, max_length=200, is_required=True),)

def loginlogout(request):
	"""
	User login and logout
	"""
	if not request.user.is_authenticated():
		manipulator = LoginForm()
		# log in user
		if request.POST:
			data = request.POST.copy()
			errors = manipulator.get_validation_errors(data)
			if not errors:
				manipulator.do_html2python(data)
				user = authenticate(username=data['login'], password=data['password'])
				if user is not None:
					login(request, user)
					return HttpResponseRedirect("/user/")
				else:
					form = forms.FormWrapper(manipulator, data, errors)
					return render_to_response(
						'userpanel/login.html',
						{'loginform': True, 'error': True, 'form': form},
						context_instance=RequestContext(request))
		# no post data, show the login form
		else:
			errors = data = {}
		form = forms.FormWrapper(manipulator, data, errors)
		if request.GET and request.GET.has_key('b'):
			return render_to_response(
				'userpanel/login.html',
				{'loginform': True, 'form': form, 'reset': True},
				context_instance=RequestContext(request))
		return render_to_response(
			'userpanel/login.html',
			{'loginform': True, 'form': form},
			context_instance=RequestContext(request))
	else:
		# user authenticated
		if request.GET:
			# logout user
			data = request.GET.copy()
			if data.has_key('log'):
				logout(request)
				return HttpResponseRedirect("/user/")
		return HttpResponseRedirect("/user/")




class PMessage(forms.Manipulator):
	"""
	Email-Messages sending manipulator
	"""
	def __init__(self):
		self.fields = (forms.TextField(field_name="subject", length=30, max_length=200, is_required=True),
		forms.LargeTextField(field_name="contents", is_required=True),)

def send_pmessage(request, target_user):
	"""
	Email-Messages sending
	"""
	if request.user.is_authenticated() and str(request.user) != str(target_user) and len(str(target_user)) > 0 and str(target_user) != 'AnonymousUser':
		ruser = User.objects.get(username=str(target_user))
		try:
			ruser_profile = Profile.objects.get(username=ruser)
		except:
			mess = False
		else:
			mess = ruser_profile.use_messages
		if not mess:
			return render_to_response(
				'pages/bug.html',
				{'bug': _('This user doesn\'t want to receive any messages')},
				context_instance=RequestContext(request))
		manipulator = PMessage()
		if request.POST:
			new_data = request.POST.copy()
			errors = manipulator.get_validation_errors(new_data)
			if not errors:
				manipulator.do_html2python(new_data)
				send_mail(new_data['subject'], new_data['contents'], request.user.email, [ruser.email], fail_silently=False)
				return HttpResponseRedirect("/user/")
		else:
			errors = new_data = {}
		form = forms.FormWrapper(manipulator, new_data, errors)
		return render_to_response('userpanel/pmessage.html', {'form': form}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/user/")

def edit_profile_pmessage(request):
	"""
	Edit profile view
	"""
	if request.user.is_authenticated():
		try:
			p = Profile.objects.get(username=request.user)
		except:
			p = Profile(username=request.user)
			p.save()
		if request.POST:
			data = request.POST.copy()
			if not data.has_key('use_messages'):
				data['use_messages'] = False
			else:
				data['use_messages'] = True
			p.use_messages = data['use_messages']
			p.save()
			return HttpResponseRedirect("/user/")
		return render_to_response('userpanel/profile_pmessage.html', {'p': p}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/user/login/")




class HMessage(forms.Manipulator):
	"""
	Password reset manipulator
	"""
	def __init__(self):
		self.fields = (forms.TextField(field_name="login", length=30, max_length=200, is_required=True),
		forms.EmailField(field_name="email", is_required=True, length=20),)

def send_hmessage(request):
	"""
	Password reset
	"""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/user/password_reset/')
	manipulator = HMessage()
	if request.POST:
		new_data = request.POST.copy()
		errors = manipulator.get_validation_errors(new_data)
		if not errors:
			manipulator.do_html2python(new_data)
			if new_data['login'].lower() == 'riklaunim' or new_data['email'].lower() == 'riklaunim@gmail.com':
				return render_to_response(
					'pages/bug.html',
					{'bug': _('ROTFL LOL OMG CSS :)')},
					context_instance=RequestContext(request))
			try:
				u = User.objects.get(username=new_data['login'], email = new_data['email'])
			except:
				return render_to_response(
					'pages/bug.html',
					{'bug': _('No such user account')},
					context_instance=RequestContext(request))
			else:
				a = User.objects.make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyz23456789')
				u.set_password(a)
				send_mail(
					_('Password reset'),
					_('Your new password on rk.edu.pl sites is: ') + a,
					'riklaunim@gmail.com',
					[new_data['email']],
					fail_silently=False)
				u.save()
			return HttpResponseRedirect("/user/login/?b=ok")
	else:
		errors = new_data = {}
	form = forms.FormWrapper(manipulator, new_data, errors)
	return render_to_response('userpanel/hmessage.html', {'form': form}, context_instance=RequestContext(request))




class ZMessage(forms.Manipulator):
	"""
	Password change manipulator
	"""
	def __init__(self):
		self.fields = (forms.TextField(field_name="haslo1", length=30, max_length=200, is_required=True, validator_list=[validators.isAlphaNumeric, self.size4, self.equal]),
		forms.TextField(field_name="haslo2", length=30, max_length=200, is_required=True),)
	def equal(self, field_data, all_data):
		if all_data['haslo2'] != field_data:
			raise validators.ValidationError(_('Passwords do not match'))
	def size4(self, field_data, all_data):
		if len(field_data) < 5:
			raise validators.ValidationError(_('To short'))

def send_zmessage(request):
	"""
	Password change
	"""
	if request.user.is_authenticated():
		if request.user.is_staff:
			return render_to_response('pages/bug.html', {'bug': _('ROTFL LOL OMG CSS :)')}, context_instance=RequestContext(request))
		manipulator = ZMessage()
		if request.POST:
			new_data = request.POST.copy()
			errors = manipulator.get_validation_errors(new_data)
			if not errors:
				manipulator.do_html2python(new_data)
				request.user.set_password(new_data['haslo1'])
				request.user.save()
				return HttpResponseRedirect("/user/")
		else:
			errors = new_data = {}
		form = forms.FormWrapper(manipulator, new_data, errors)
		return render_to_response('userpanel/zmessage.html', {'form': form}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/user/login/")