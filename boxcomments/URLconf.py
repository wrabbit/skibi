from django.conf.urls.defaults import *
from django.conf import settings
from boxcomments.models import Comment


info_dict={
        'queryset':Comment.objects.all(),
        'template_name':'boxcomments/comments_szczegoly.html',
		'extra_context':{ 'header':'Komentarze','com':'com'},
	}


urlpatterns = patterns('boxcomments',
(r'^(?P<appid>[0-9]+)/(?P<apptype>[0-9]+)/(?P<quoteid>[0-9]+)/add', 'views.comments',{'add':True,'header':'Dodaj komentarz'}),
(r'^(?P<appid>[0-9]+)/(?P<apptype>[0-9]+)/add/', 'views.comments',{'add':True,'header':'Dodaj komentarz'}),
(r'^(?P<appid>[0-9]+)/(?P<apptype>[0-9]+)/', 'views.comments'),
)
urlpatterns += patterns('',
(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',info_dict),

)