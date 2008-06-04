#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum

from re import findall
import base64
from datetime import datetime
from stripogram import html2safehtml

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import newforms as forms
from django.conf import settings
from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django.db.models import Q
from django.core.mail import mail_admins
from django.contrib.auth.decorators import login_required

from myghtyboard.models import *


def list_perms(request):
	"""
	list permissions used in templates
	"""
	perms = {}
	if request.user.is_authenticated():
		perms['add_topic'] = True
		perms['add_post'] = True
		perms['is_authenticated'] = True
		perms['is_staff'] = request.user.is_staff
	else:
		perms['add_topic'] = False
		perms['add_post'] = False
		perms['is_staff'] = False
	return perms


def category_list(request):
	"""
	show all categories and their topics
	"""
	categories = Category.objects.all().order_by('cat_order')
	for c in categories:
		c.forums = c.forum_set.all().order_by('forum_order')
	return render_to_response(
		'myghtyboard/category_list.html',
		{'categories': categories, 'perms': list_perms(request)},
		context_instance=RequestContext(request))


def topic_list(request, forum_id, pagination_id=1):
	"""
	list of topics in a forum
	
	* forum_id - id of a Forum record
	"""
	try:
		topics = Topic.objects.order_by('-is_global', '-is_sticky', '-topic_modification_date').filter(Q(topic_forum=forum_id) | Q(is_global='1'))
		forum_name = Forum.objects.get(id=forum_id)
		forum_name = forum_name.forum_name
	except:
		return HttpResponseRedirect('/forum/')
	return object_list(
		request,
		Topic.objects.order_by('-is_global', '-is_sticky', '-topic_modification_date').filter(Q(topic_forum=forum_id) | Q(is_global='1')),
		paginate_by = 10,
		allow_empty = True,
		page = pagination_id,
		extra_context = {'forum': forum_id,  'perms': list_perms(request), 'forum_name': forum_name},
		template_name = 'myghtyboard/topics_list.html')


def my_topic_list(request, show_user=False):
	"""
	list my topics
	
	* show_user - if not set will show current user topics
	"""
	if not show_user:
		show_user = str(request.user)
	if request.user.is_authenticated():
		topics = Topic.objects.order_by('-topic_modification_date').filter(topic_author=show_user)[:50]
		forum_name = _('User Topics')
		return render_to_response(
			'myghtyboard/mytopics_list.html',
			{'topics': topics, 'forum_name': forum_name, 'perms': list_perms(request)},
			context_instance=RequestContext(request))
	else:
		return render_to_response('pages/bug.html', {'bug': _('You aren\'t logged in')}, context_instance=RequestContext(request))

@login_required
def last_topic_list(request):
	"""
	 list last active topics
	"""
	topics = Topic.objects.order_by('-topic_modification_date')[:50]
	for i in topics:
		pmax =  i.post_set.all().count()/10
		pmaxten =  i.post_set.all().count()%10
		if pmaxten != 0:
			i.pagination_max = pmax+1
		else:
			i.pagination_max = pmax
	forum_name = _('Last Active Topics')
	return render_to_response(
		'myghtyboard/mytopics_list.html',
		{'topics': topics, 'forum_name': forum_name, 'perms': list_perms(request)},
		context_instance=RequestContext(request))

@login_required
def my_posttopic_list(request, show_user=False):
	"""
	list topics with my posts
	
	* show_user - if not set will show current user topics
	"""
	if not show_user:
		show_user = str(request.user)
	try:
		topics = Post.objects.order_by('-post_date').filter(post_author=show_user).values('post_topic').distinct()[:50]
		posts = []
		for i in topics:
			posts.append(int(i['post_topic']))
		topics = Topic.objects.order_by('-topic_modification_date').filter(id__in=posts)
		for i in topics:
			pmax =  i.post_set.all().count()/10
			pmaxten =  i.post_set.all().count()%10
			if pmaxten != 0:
				i.pagination_max = pmax+1
			else:
				i.pagination_max = pmax
		forum_name = _('User Posts in Latest Topics')
	except:
		return render_to_response('myghtyboard/mytopics_list.html', {'perms': list_perms(request)}, context_instance=RequestContext(request))
	return render_to_response(
		'myghtyboard/mytopics_list.html',
		{'topics': topics, 'forum_name': forum_name, 'perms': list_perms(request)},
		context_instance=RequestContext(request))


def post_list(request, topic_id, pagination_id):
	"""
	 list post in topic with a generic pagination view
	
	* topic_id - id of a Topic entry
	"""
	try:
		topic = Topic.objects.get(id=topic_id)
	except Topic.DoesNotExist:
		return HttpResponseRedirect('/forum/')
	if  topic.is_locked:
		opened = False
	else:
		opened = True
	return object_list(
		request,
		topic.post_set.all().order_by('post_date'),
		paginate_by = 10,
		page = pagination_id,
		extra_context = {
			'topic_id':topic_id,
			'opened': opened,
			'topic': topic.topic_name,
			'forum_id': topic.topic_forum.id,
			'forum_name': topic.topic_forum,
			'perms': list_perms(request),
			'current_user': str(request.user)},
		template_name = 'myghtyboard/post_list.html')

class AddTopicForm(forms.ModelForm):
	class Meta:
		model = Topic

@login_required
def add_topic(request, forum_id):
	"""
	add topic
	
	* forum_id - ID of a Forum entry
	"""
	
	
	if request.POST:
		page_data = request.POST.copy()
		page_data['topic_author'] = str(request.user)
		tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['text'])
		for i in tags:
			page_data['text'] = page_data['text'].replace(u'[code]'+i+u'[/code]', u'[code]'+base64.encodestring(i)+u'[/code]')
		page_data['text'] = html2safehtml(page_data['text'] ,valid_tags=settings.VALID_TAGS)
		tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['text'])
		for i in tags:
			page_data['text'] = page_data['text'].replace(u'[code]'+i+u'[/code]', u'[code]'+base64.decodestring(i)+u'[/code]')
		text = page_data['text']
		del page_data['text']
		page_data['topic_name'] = html2safehtml(page_data['topic_name'] ,valid_tags=())
		page_data['topic_forum'] = forum_id
		page_data['topic_posts'] = 1
		page_data['topic_lastpost'] = str(request.user)+'<br />' + str(datetime.today())[:-10]
		page_data['topic_last_pagination_page'] = 1
		page_data['topic_modification_date'] = datetime.now()
		form = AddTopicForm(page_data)
		if form.is_valid():
			new_place = form.save()
			post = Post(post_topic = new_place, post_text = text, post_author = str(request.user), post_ip = request.META['REMOTE_ADDR'])
			post.save()
			forum = Forum.objects.get(id=forum_id)
			forum.forum_topics = forum.forum_topics +1
			forum.forum_posts = forum.forum_posts +1
			forum.forum_lastpost = str(request.user)+' (' + str(datetime.today())[:-10] + ')<br /><a href="/forum/topic/1/' + str(new_place.id) + '/">' + new_place.topic_name + '</a>'
			forum.save()
			
			mail_admins('Temat Dodany', "Dodano Temat: http://www." + settings.SITE_KEY + "/forum/forum/" + forum_id +"/", fail_silently=True)
			
			return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
		else:
			return render_to_response(
				'myghtyboard/add_topic.html',
				{'form': form, 'perms': list_perms(request)},
				context_instance=RequestContext(request))
	
	form = AddTopicForm()
	return render_to_response(
		'myghtyboard/add_topic.html',
		{'form': form, 'perms': list_perms(request)},
		context_instance=RequestContext(request))

class AddPostForm(forms.ModelForm):
	class Meta:
		model = Post

@login_required
def add_post(request, topic_id, post_id = False):
	"""
	add post
	
	* topic_id - id of a Topic entry
	* post_id - id of a Post entry to be quoted
	"""
	
	topic = Topic.objects.values('is_locked').get(id=topic_id)
	if topic['is_locked']:
		return render_to_response('pages/bug.html', {'bug': _('Topic is closed')}, context_instance=RequestContext(request))

	# check who made the last post.
	lastpost = Post.objects.order_by('-post_date').filter(post_topic=topic_id)[:1]
	is_staff = request.user.is_staff
	# if the last poster is the current one (login) and he isn't staff then we don't let him post after his post
	if str(lastpost[0].post_author) == str(request.user) and not is_staff:
		return render_to_response('pages/bug.html', {'bug': _('You can\'t post after your post')}, context_instance=RequestContext(request))
	
	lastpost = Post.objects.filter(post_topic=topic_id).order_by('-id')[:10]
	if request.POST:
		page_data = request.POST.copy()
		page_data['post_author'] = str(request.user)
		tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'])
		for i in tags:
			page_data['post_text'] = page_data['post_text'].replace(u'[code]'+i+u'[/code]', u'[code]'+base64.encodestring(i)+u'[/code]')
		page_data['post_text'] = html2safehtml(page_data['post_text'] ,valid_tags=settings.VALID_TAGS)
		tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'])
		for i in tags:
			page_data['post_text'] = page_data['post_text'].replace(u'[code]'+i+u'[/code]', u'[code]'+base64.decodestring(i)+u'[/code]')
		
		page_data['post_ip'] = request.META['REMOTE_ADDR']
		page_data['post_topic'] = topic_id
		page_data['post_date'] = datetime.now()
		form = AddPostForm(page_data)
		if form.is_valid():
			form.save()
		
			topic = Topic.objects.get(id=topic_id)
			posts = Post.objects.filter(post_topic=topic_id).count()
			
			pmax =  posts/10
			pmaxten =  posts%10
			if pmaxten != 0:
				pmax = pmax+1
				topic.topic_last_pagination_page = pmax
			elif pmax > 0:
				topic.topic_last_pagination_page = pmax
			else:
				pmax = 1
				topic.topic_last_pagination_page = 1
			topic.topic_posts = posts
			topic.topic_lastpost = str(request.user)+'<br />' + str(datetime.today())[:-10]
			topic.save()
			
			forum = Forum.objects.get(id=topic.topic_forum.id)
			forum.forum_posts = forum.forum_posts +1
			
			forum.forum_lastpost = str(request.user)+' (' + str(datetime.today())[:-10] + ')<br /><a href="/forum/topic/' + str(pmax) + '/' + str(topic.id) + '/">' + topic.topic_name + '</a>'
			forum.save()
			
			mail_admins('Post Dodany', "Dodano Post: http://www." + settings.SITE_KEY + "/forum/topic/" + str(pmax) + "/" + topic_id +"/", fail_silently=True)
			return HttpResponseRedirect("/forum/topic/" + str(pmax) + "/" + topic_id +"/")
		else:
			return render_to_response(
				'myghtyboard/add_post.html',
				{'lastpost': lastpost, 'perms': list_perms(request), 'form':form},
				context_instance=RequestContext(request))
	else:
		if post_id:
			quote = Post.objects.get(id=post_id)
			quote_text = '<blockquote><b>' + quote.post_author + _(' wrote') + ':</b><br /><cite>' + quote.post_text + '</cite></blockquote>\n\n'
		else:
			quote_text = ''
	return render_to_response(
		'myghtyboard/add_post.html',
		{'quote_text': quote_text, 'lastpost': lastpost, 'perms': list_perms(request)},
		context_instance=RequestContext(request))

@login_required
def edit_post(request, post_id):
	"""
	edit post
	
	* post_id - id of a Post entry
	"""
	
	post = Post.objects.get(id=post_id)
	topic = Topic.objects.values('is_locked').get(id=post.post_topic.id)
	if topic['is_locked']:
		return render_to_response('pages/bug.html', {'bug': _('Topic is closed')}, context_instance=RequestContext(request)) # locked topic!
	
	if str(request.user) == post.post_author or  request.user.is_staff:
		if request.POST and len(request.POST.copy()['post_text']) > 1:
			page_data = request.POST.copy()
			tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'])
			for i in tags:
				page_data['post_text'] = page_data['post_text'].replace(u'[code]'+i+u'[/code]', u'[code]'+base64.encodestring(i)+u'[/code]')
			page_data['post_text'] = html2safehtml(page_data['post_text'] ,valid_tags=settings.VALID_TAGS)
			tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'])
			for i in tags:
				page_data['post_text'] = page_data['post_text'].replace(u'[code]'+i+u'[/code]', u'[code]'+base64.decodestring(i)+u'[/code]')
			post.post_text = page_data['post_text']
			post.save()
			
			pmax = Post.objects.filter(post_topic=post.post_topic).count()/10
			pmaxten =  Post.objects.filter(post_topic=post.post_topic).count()%10
			if pmaxten != 0:
				pmax = pmax+1
			return HttpResponseRedirect("/forum/topic/" + str(pmax) + "/" + str(post.post_topic.id) +"/")
		else:
			return render_to_response(
				'myghtyboard/edit_post.html',
				{'post_text': post.post_text, 'perms': list_perms(request)},
				context_instance=RequestContext(request))
	else:
		return render_to_response('pages/bug.html', {'bug': _('You can\'t edit this post')}, context_instance=RequestContext(request)) # can't edit post


def delete_post(request, post_id, topic_id):
	"""
	delete a post
	
	* post_id - ID of a Post entry
	* topic_id - Topic entry ID that contain the Post entry
	"""
	if request.user.is_authenticated() and request.user.is_staff:
		Post.objects.get(id=post_id).delete()
		topic = Topic.objects.get(id=topic_id)
		topic.topic_posts = topic.topic_posts -1
		topic.save()
		return HttpResponseRedirect("/forum/topic/1/" + topic_id +"/")
	else:
		return render_to_response('pages/bug.html', {'bug': _('You aren\'t a moderator')}, context_instance=RequestContext(request))


def delete_topic(request, topic_id, forum_id):
	"""
	delete a topic with all posts
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	if request.user.is_authenticated() and request.user.is_staff:
		posts = Post.objects.filter(post_topic=topic_id).count()
		Topic.objects.get(id=topic_id).delete()
		Post.objects.filter(post_topic=topic_id).delete()
		forum = Forum.objects.get(id=forum_id)
		forum.forum_topics = forum.forum_topics -1
		forum.forum_posts = forum.forum_posts - posts
		forum.save()
		return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
	else:
		return render_to_response('pages/bug.html', {'bug': _('You aren\'t a moderator')}, context_instance=RequestContext(request))


def move_topic(request, topic_id, forum_id):
	"""
	move topic
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	if request.user.is_authenticated() and request.user.is_staff:
		if request.POST and len(request.POST['forum']) > 0:
			topic = Topic.objects.get(id=topic_id)
			topic.topic_forum=Forum.objects.get(id=request.POST['forum'])
			topic.save()
			t = Topic(
				topic_forum=Forum.objects.get(id=forum_id),
				topic_name = topic.topic_name,
				topic_author = topic.topic_author,
				topic_posts = 0,
				topic_lastpost = _('Topic Moved'),
				is_locked = True)
			t.save()
			p = Post(
				post_topic = t,
				post_text = _('This topic has been moved to another forum. To see the topic follow') + ' <a href="/forum/topic/1/' + str(topic_id) +'/"><b>' + _('this link') + '</b></a>',
				post_author = _('Forum Staff'),
				post_ip = str(request.META['REMOTE_ADDR']))
			p.save()
			return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
		else:
			forums = Forum.objects.exclude(id=forum_id)
			topic = Topic.objects.get(id=topic_id)
			return render_to_response(
				'myghtyboard/move_topic.html',
				{'forums': forums, 'topic': topic, 'perms': list_perms(request)},
				context_instance=RequestContext(request))
	else:
		return render_to_response('pages/bug.html', {'bug': _('You aren\'t a moderator')}, context_instance=RequestContext(request)) # can't move


def close_topic(request, topic_id, forum_id):
	"""
	close topic
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	if request.user.is_authenticated() and request.user.is_staff:
		topic = Topic.objects.get(id=topic_id)
		topic.is_locked=True
		topic.save()
		return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
	else:
		return render_to_response('pages/bug.html', {'bug': _('You aren\'t a moderator')}, context_instance=RequestContext(request))


def open_topic(request, topic_id, forum_id):
	"""
	open topic
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	if request.user.is_authenticated() and request.user.is_staff:
		topic = Topic.objects.get(id=topic_id)
		topic.is_locked=False
		topic.save()
		return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
	else:
		return render_to_response('pages/bug.html', {'bug': _('You aren\'t a moderator and you aren\'t logged in')}, context_instance=RequestContext(request))
