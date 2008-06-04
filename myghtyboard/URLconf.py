from django.conf.urls.defaults import *

# Myghtyboard URLs
urlpatterns = patterns('myghtyboard',
(r'^$', 'views.category_list'),
(r'^forum/(?P<forum_id>[0-9]+)/$', 'views.topic_list'),
(r'^forum/(?P<forum_id>[0-9]+)/(?P<pagination_id>[0-9]+)/$', 'views.topic_list'),
(r'^add_topic/(?P<forum_id>[0-9]+)/$', 'views.add_topic'),
(r'^add_post/(?P<topic_id>[0-9]+)/(?P<post_id>[0-9]+)/$', 'views.add_post'), # add post with quote
(r'^add_post/(?P<topic_id>[0-9]+)/$', 'views.add_post'),
(r'^edit_post/(?P<post_id>[0-9]+)/$', 'views.edit_post'),
(r'^delete_post/(?P<post_id>[0-9]+)/(?P<topic_id>[0-9]+)/$', 'views.delete_post'),
(r'^move_topic/(?P<topic_id>[0-9]+)/(?P<forum_id>[0-9]+)/$', 'views.move_topic'),
(r'^delete_topic/(?P<topic_id>[0-9]+)/(?P<forum_id>[0-9]+)/$', 'views.delete_topic'),
(r'^close_topic/(?P<topic_id>[0-9]+)/(?P<forum_id>[0-9]+)/$', 'views.close_topic'),
(r'^open_topic/(?P<topic_id>[0-9]+)/(?P<forum_id>[0-9]+)/$', 'views.open_topic'),
(r'^topic/(?P<pagination_id>[0-9]+)/(?P<topic_id>[0-9]+)/$', 'views.post_list'),
(r'^mytopics/(?P<show_user>.*)/$', 'views.my_topic_list'),
(r'^mytopics/$', 'views.my_topic_list'),
(r'^lasttopics/$', 'views.last_topic_list'),
(r'^myptopics/(?P<show_user>.*)/$', 'views.my_posttopic_list'),
(r'^myptopics/$', 'views.my_posttopic_list'),
)
