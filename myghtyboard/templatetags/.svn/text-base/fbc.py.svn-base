#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum

from re import findall
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter

from django import template
from django.conf import settings

register = template.Library()

def fbc(value):
	"""
	Parse emotes, BBcode and format [code] blocks
	"""
	value = value.replace(':omg:', '<img src="/site_media/layout/forum/smilies/icon_eek.gif" alt="" />')
	value = value.replace(':nice:', '<img src="/site_media/layout/forum/smilies/icon_biggrin.gif" alt="" />')
	value = value.replace(':evil:', '<img src="/site_media/layout/forum/smilies/icon_evil.gif" alt="" />')
	value = value.replace(':twisted:', '<img src="/site_media/layout/forum/smilies/icon_twisted.gif" alt="" />')
	value = value.replace(':grin:', '<img src="/site_media/layout/forum/smilies/icon_cheesygrin.gif" alt="" />')
	value = value.replace(':cool:', '<img src="/site_media/layout/forum/smilies/icon_cool.gif" alt="" />')
	value = value.replace('[b]', '<b>')
	value = value.replace('[/b]', '</b>')
	value = value.replace('[i]', '<i>')
	value = value.replace('[/i]', '</i>')
	value = value.replace('[u]', '<u>')
	value = value.replace('[/u]', '</u>')
	value = value.replace('[quote]', '<blockquote>')
	value = value.replace('[/quote]', '</blockquote>')
	value = value.replace('[url]', '')
	value = value.replace('[/url]', '')
	
	value = value.replace('\n', '<br />')
	tags = findall( r'(?xs)\[code\](.*?)\[/code]''', value)
	for i in tags:
		j = i.replace('<br />', '')
		value = value.replace('[code]' + i + '[/code]', '<div class="box" style="overflow:auto;font-size:10px;background-color:#EEEEEE;">' + highlight(j, HtmlLexer(), HtmlFormatter()) + '</div><style>' + HtmlFormatter().get_style_defs('.highlight') + '</style>')
	return value

register.filter('fbc', fbc)