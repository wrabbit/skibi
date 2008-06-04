#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _


class Category(models.Model):
	cat_name = models.CharField(max_length=255, verbose_name=_("Category Name"))
	cat_order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Order"))
	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")
		db_table = 'rk_category' + str(settings.SITE_ID)
	class Admin:
		list_display = ('cat_name','cat_order')
	def __str__(self):
		return self.cat_name
	def __unicode__(self):
		return self.cat_name

class Forum(models.Model):
	forum_category = models.ForeignKey(Category, verbose_name=_("Forum Category"))
	forum_name = models.CharField(max_length=255, verbose_name=_("Forum Name"))
	forum_description = models.CharField(max_length=255, verbose_name=_("Forum Description"))
	forum_topics = models.PositiveIntegerField(blank=True,default=0, verbose_name=_("Topics"))
	forum_posts = models.PositiveIntegerField(blank=True,default=0, verbose_name=_("Posts"))
	forum_lastpost = models.CharField(max_length=255, verbose_name=_("Last Post"), blank=True, default='', null=True)
	forum_order = models.PositiveSmallIntegerField(default=0)
	class Meta:
		verbose_name = _("Forum")
		verbose_name_plural = _("Forums")
		db_table = 'rk_forum' + str(settings.SITE_ID)
	class Admin:
		list_display = ('forum_name', 'forum_description', 'forum_category', 'forum_order')
		fields = (
		(None, {
		'fields': ('forum_category', 'forum_name', 'forum_description', 'forum_order')
		}),
		(_('Stats'), {'fields': ('forum_topics', 'forum_posts'), 'classes': 'collapse'}),)
	def __str__(self):
		return self.forum_name
	def __unicode__(self):
		return self.forum_name

class Topic(models.Model):
	topic_forum = models.ForeignKey(Forum, verbose_name=_("Forum"))
	topic_name = models.CharField(max_length=255, verbose_name=_("Topic Title"))
	topic_author = models.CharField(max_length=255, verbose_name=_("Author"), blank=True)
	topic_posts = models.PositiveIntegerField(default=0, blank=True, verbose_name=_("Posts"))
	topic_lastpost = models.CharField(max_length=255, verbose_name=_("Last Post"))
	topic_modification_date = models.DateTimeField(default=datetime.now())
	topic_last_pagination_page = models.PositiveIntegerField(default=1, blank=True, verbose_name=_("Pagination Page"))
	is_sticky = models.BooleanField(blank=True, default=False)
	is_locked = models.BooleanField(blank=True, default=False)
	is_global = models.BooleanField(blank=True, default=False)
	class Meta:
		verbose_name = _("Topic")
		verbose_name_plural = _("Topics")
		db_table = 'rk_topic' + str(settings.SITE_ID)
	def __str__(self):
		return self.topic_name
	def __unicode__(self):
		return self.topic_name
	def save(self, **kwargs):
		"""override save to set defaults"""
		if self.pk:
			self.topic_modification_date = datetime.now()
		super(Topic, self).save(**kwargs)

class Post(models.Model):
	post_topic = models.ForeignKey(Topic, verbose_name=_("Post"))
	post_text = models.TextField() # the post text
	post_author = models.CharField(max_length=255, verbose_name=_("Author"), blank=True)
	post_date = models.DateTimeField(default=datetime.now, blank=True)
	post_ip = models.CharField(max_length=20, blank=True)
	class Meta:
		verbose_name = _("Post")
		verbose_name_plural = _("Posts")
		db_table = 'rk_post' + str(settings.SITE_ID)
	def __str__(self):
		return str(self.id)
	def __unicode__(self):
		return unicode(self.id)
