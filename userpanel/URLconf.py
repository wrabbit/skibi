from django.conf.urls.defaults import *

urlpatterns = patterns('userpanel',
(r'^$', 'views.user_panel',{'header':'Panel użytkownika'}),
(r'^pmessage/(?P<target_user>.*)/$', 'views.send_pmessage',{'header':'Wyślij wiadomość'}),
(r'^userlist/$', 'views.userlist',{'header':'Lista użytkowników'}),
(r'^uprawnienia/$', 'views.permissions_list',{'header':'Moje uprawnienia'}),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^theme/$', 'direct_to_template', {'template': 'userpanel/theme.html','header':'Zmiana wyglądu'}),

	
)


