#!/usr/bin/python
# Diamanda Application Set
# User Panel

from datetime import timedelta
from datetime import datetime

from django.http import HttpResponse
from django.conf import settings

from userpanel.models import *

class userMiddleware(object):
	"""
	Update user onsitedata when he is on site (to display "users online")
	"""
	def process_request(self, request):
		if request.user.is_authenticated():
			now = datetime.now()
			check_time = now - timedelta(hours=1)
			if not request.session.__contains__('onsite') or request.session['onsite'] < check_time:
				request.session['onsite'] = now
				try:
					a = Profile.objects.get(username=request.user)
					a.save()
				except:
					a = Profile(username=request.user)
					a.save()
