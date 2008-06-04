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


def user_panel(request,header):
	"""
	main user panel
	"""
	from django.conf import settings
	admin_mail = settings.SERVER_EMAIL 
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/user/login/")
	return render_to_response('userpanel/panel.html', {'header':header,'admin_mail':admin_mail},context_instance=RequestContext(request))

def userlist(request,header):
	"""
	list all users
	"""
	users = User.objects.all()
	return object_list(request, users, extra_context={'header':header},paginate_by = 25, allow_empty = True, template_name = 'userpanel/userlist.html')

def permissions_list(request,header):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        p = request.user.get_all_permissions()
        return render_to_response('userpanel/my_perm.html',{'perm':p,'header':header},context_instance=RequestContext(request))


class PMessage(forms.Manipulator):
	"""
	Email-Messages sending manipulator
	"""
	def __init__(self):
		self.fields = (forms.TextField(field_name="subject", length=30, max_length=200, is_required=True),
		forms.LargeTextField(field_name="contents", is_required=True),)

def send_pmessage(request, target_user,header):
	"""
	Email-Messages sending
	"""
	if request.user.is_authenticated() and str(request.user) != str(target_user) and len(str(target_user)) > 0 and str(target_user) != 'AnonymousUser':
		ruser = User.objects.get(username=str(target_user))

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
		return render_to_response('userpanel/pmessage.html', {'form': form,'header':header}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/user/")



