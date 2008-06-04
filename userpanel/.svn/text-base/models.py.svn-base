#!/usr/bin/python
# Diamanda Application Set
# User Panel
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	username = models.ForeignKey(User)
	onsitedata = models.DateTimeField(default=datetime.now(), blank=True)
	use_messages =  models.BooleanField(blank=True, default=True)
	def __str__(self):
		return str(self.username)
	def __unicode__(self):
		return unicode(self.username)
	def save(self, **kwargs):
		"""override save to set defaults"""
		if self.pk:
			self.onsitedata = datetime.now()
		super(Profile, self).save(**kwargs)