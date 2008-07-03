from django.conf.urls.defaults import *
from e_szkola.e_dziennik.models import *
from django.contrib.auth.models import *
from e_szkola.e_dziennik.feeds import *
from django.contrib.sitemaps import FlatPageSitemap
from django.views.generic.date_based import archive_index,archive_year, archive_month
feeds = {
    'news': LatestNews,
}
info_dict={
        'queryset':Klasy.objects.all().order_by('-id'),
        'template_name':'base_tresc.html',
		'extra_context':{ 'header':'Uwagi'},
	}
info_dict_1={
        'queryset':Uczniowie_tmp.objects.all().order_by('-id'),
        'template_name':'uwagi_list.html',
		'extra_context':{ 'header':'Uwagi'},
	}
info_dict_2={
        'queryset':Aktualnosci.objects.all(),
        'template_name':'news.html',
		'extra_context':{ 'header':'Aktualności'},
	}
news_archives = {
    'queryset'   : Aktualnosci.objects.all(),
    'date_field' : 'news_date',
	#'template_name' : 'news_archive.html',
}
urlpatterns = patterns('',
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^admin/', include('django.contrib.admin.urls')),
	(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': 'site_media'}),
	(r'^/?$', 'django.views.generic.list_detail.object_list', {'queryset':Demo.objects.all().order_by('-id'), 'paginate_by':10, 'allow_empty':True, 'template_name':'login/login_tresc.html'}),
	(r'^(?P<object_id>\d+)/uczniowie/$', 'django.views.generic.list_detail.object_detail',info_dict),
	(r'^(?P<object_id>\d+)/sprawdz/uwagi/$', 'django.views.generic.list_detail.object_detail',info_dict_1),
	(r'^news/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',info_dict_2),
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+).xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	(r'^com/', include('boxcomments.URLconf')),
	(r'^forum/', include('myghtyboard.URLconf')),
	(r'^user/', include('userpanel.URLconf')),
	(r'^cal/', include('cal.urls')),
	(r'^archives/(?P<year>\d{4})/(?P<month>\d{2})/$',archive_month,dict(news_archives,month_format='%m')),
	(r'^archives/(?P<year>\d{4})/?$',archive_year,dict(news_archives,make_object_list=True)),
	(r'^archives/',archive_index,news_archives),


	
	
)

urlpatterns += patterns('e_dziennik.all',

   
	(r'^loged/$', 'pobierz_dane'),	
	(r'^loged/(?P<page>[0-9]+)/$', 'pobierz_dane'),	
	(r'^wyloguj/$', 'wyloguj'),
	(r'^(?P<klasa_id>\d+)/$','wczytaj_menu'),
	(r'^(?P<klasa_id>\d+)/password_change/$', 'password_change',{'header': 'Zmiana hasła'}),
	(r'^(?P<klasa_id>\d+)/password_change/done/$', 'password_change_done'),
	(r'^(?P<klasa_id>\d+)/email_send/$', 'email_send',{'header': 'Poczta'}),
	(r'^(?P<klasa_id>\d+)/email_send/done/$', 'email_send_done'),
	(r'^sprawdz_msg/$', 'sprawdz_msg',{'header':'System wiadomości'}),
    (r'^sprawdz_msg/(?P<page>[0-9]+)/$', 'sprawdz_msg',{'header':'System wiadomości'}),
	(r'^(?P<klasa_id>\d+)/message_send/$', 'message_send',{'header': 'System wiadomości'}),
	(r'^(?P<klasa_id>\d+)/message_send/done/$', 'message_send_done'),
	(r'^(?P<klasa_id>\d+)/del/(?P<msg_id>\d+)/$', 'usun_msg'),
	(r'^(?P<user_id>\d+)/historia/$', 'historia_zdarzen',{'header':'Historia zdarzeń'}),
	(r'^(?P<user_id>\d+)/historia/(?P<page>[0-9]+)/$', 'historia_zdarzen',{'header':'Historia zdarzeń'}),
	
)
urlpatterns += patterns('e_dziennik.wych',
   
    #(r'^accounts/create/$', 'register'),
	#(r'^accounts/confirm/(?P<activation_key>.*)/$', 'confirm'),
	(r'^(?P<klasa_id>\d+)/(?P<klucz>\D+)/add/(?P<uczen_id>\d+)/$', 'dodaj_rodzica'),
	(r'^(?P<klasa_id>\d+)/(?P<klucz>\D+)/add/$', 'dodaj'),
	(r'^(?P<klasa_id>\d+)/(?P<klucz>\D+)/edit/(?P<r_id>\d+)/$', 'edytuj'),
	(r'^(?P<klasa_id>\d+)/(?P<klucz>\D+)/edit_r/(?P<rod_id>\d+)/(?P<r_id>\d+)/$', 'edytuj_rodzica'),
	(r'^(?P<klasa_id>\d+)/(?P<klucz>\D+)/del/(?P<r_id>\d+)/$', 'usun'),
	(r'^(?P<klasa_id>\d+)/Lista uczniow/add_plik/$', 'dane_z_pliku'),
	(r'^(?P<klasa_id>\d+)/Nieobecnosci/$', 'wyswietl_nieobecnosci'),
	(r'^(?P<klasa_id>\d+)/add/nieobecnosci/$', 'dodaj_nieobecnosci'),
	(r'^(?P<klasa_id>\d+)/Plan/$', 'wyswietl_plan'),
	(r'^(?P<klasa_id>\d+)/Plan/(?P<godzina_id>\d+)/(?P<dzien>\d+)/(?P<edit>.*)$', 'dodaj_lekcje'),
	(r'^(?P<klasa_id>\d+)/Oceny/$', 'wyswietl_oceny'),
	(r'^(?P<klasa_id>\d+)/kartki/$', 'zapisz_kartki'),
	(r'^(?P<klasa_id>\d+)/Tematy/$', 'wyswietl_tematy'),
	(r'^(?P<klasa_id>\d+)/Oceny/(?P<semestr_id>\d+)/(?P<przedmiot_id>\d+)/$', 'wstaw_oceny'),
	(r'^raporty/(?P<klasa_id>\d+)/(?P<typ>\D+)/(?P<podtyp>\D+)/$', 'wyswietl_raporty'),
	(r'^add/uwagi/(?P<uczen_id>\d+)/$', 'dodaj_uwage'),
	(r'^edit/uwagi/(?P<uczen_id>\d+)/(?P<uwaga_id>\d+)/$', 'edytuj_uwage'),
	(r'^del/(?P<uwaga_id>\d+)/(?P<uczen_id>\d+)/$', 'usun_uwage'),
    (r'^(?P<klasa_id>\d+)/(?P<klucz>\D+)/$', 'wyswietl'), 
	(r'^filter/(?P<klasa_id>\d+)/(?P<plec>\D+)/$', 'filtruj_plec'),
	(r'^validate/login/(?P<login>.+)/$', 'check_login'),


)

urlpatterns += patterns('e_dziennik.rod',
    (r'^rod/(?P<uczen_id>\d+)/oceny/$', 'oceny_ucznia'),
	(r'^rod/nieobecnosci/$', 'nieobecnosci_ucznia',{'header':'Nieobecności ucznia'}),
	(r'^rod/nieobecnosci/(?P<uczen_id>\d+)/$', 'nieobecnosci_szczegoly'),
	
    (r'^potwierdz/(?P<potwierdz>\d+)/(?P<uwaga_id>\d+)/$', 'zapisz_potwierdzenie'),

	
)
urlpatterns += patterns('django.views.generic.simple',
    (r'^perm/(?P<model>\D+)/$', 'direct_to_template', {'template': 'permission_denied.html'}),
	(r'^raporty/$', 'direct_to_template', {'template': 'rodzaje_wykresow.html'}),
	(r'^full_image/(?P<obraz>.*)/$', 'direct_to_template', {'template': 'image.html'})
	
)










