from e_dziennik.models import *
from django.contrib.syndication.feeds import Feed
from django.contrib.sitemaps import Sitemap

class LatestNews(Feed):
	title = 'Aktualności z www.e-dziennik.one.pl'
	link = '/rss/news'
	description = 'Aktualności z www.e-dziennik.one.pl'
	def items(self):
		return Aktualnosci.objects.order_by('-id')[:15]
        '''
	def item_link(self,item):
            return '/news/' + str(self.id) + '/'
        '''


class NewsMap(Sitemap):
	def items( self ):
		return Aktualnosci.objects.all()
	def lastmod( self, obj ):
		return obj.news_date
	def changefreq(self, obj):
		return 'weekly'
