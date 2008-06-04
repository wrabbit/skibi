from django.conf.urls.defaults import *

urlpatterns = patterns('userpanel',
(r'^$', 'views.user_panel'),
(r'^pmessage/(?P<target_user>.*)/$', 'views.send_pmessage'),
(r'^login/$', 'views.loginlogout'),
(r'^register/$', 'views.register'),
(r'^edit/$', 'views.edit_profile_pmessage'),
(r'^userlist/$', 'views.userlist'),
(r'^password_reset/$', 'views.send_hmessage'),
(r'^password_change/$', 'views.send_zmessage'),
)
