from stats.models import Stat,UserActivity
from django.conf import settings
from datetime import datetime

class statsMiddleware(object):
	def process_request(self, request):
		try:
			today = str(datetime.today())[:10]
			unique = Stat.objects.filter(ip = request.META['REMOTE_ADDR'], date = today).count()
			if unique < 1:
				if not request.META.has_key('HTTP_REFERER'):
					request.META['HTTP_REFERER'] = ''
				s = Stat(ip = request.META['REMOTE_ADDR'], referer = request.META['HTTP_REFERER'], date = today)
				s.save()
		except:
			pass



import re
from operator import add
from time import time
from django.db import connection

class StatsSiteMiddleware(object):
        # total,python,db,queries
    def process_view(self, request, view_func, view_args, view_kwargs):

        # turn on debugging in db backend to capture time
        from django.conf import settings
        debug = settings.DEBUG
        settings.DEBUG = True

        # get number of db queries before we do anything
        n = len(connection.queries)

        # time the view
        start = time()
        response = view_func(request, *view_args, **view_kwargs)
        totTime = time() - start

        # compute the db time for the queries just run
        queries = len(connection.queries) - n
        if queries:
            dbTime = reduce(add, [float(q['time']) 
                                  for q in connection.queries[n:]])
        else:
            dbTime = 0.0

        # and backout python time
        pyTime = totTime - dbTime

        # restore debugging setting
        settings.DEBUG = debug

        stats = {
            'totTime': totTime,
            'pyTime': pyTime,
            'dbTime': dbTime,
            'queries': queries,
            }

        # replace the comment if found            
        if response and response.content:
            s = response.content
            regexp = re.compile(r'(?P<cmt><!--\s*STATS:(?P<fmt>.*?)-->)')
            match = regexp.search(s)
            if match:
                s = s[:match.start('cmt')] + \
                    match.group('fmt') % stats + \
                    s[match.end('cmt'):]
                response.content = s

        return response

		
from django.conf import settings
from django.contrib import auth
from datetime import datetime, timedelta

class AutoLogout:
  def process_request(self, request):
    if not request.user.is_authenticated() :
      #Can't log out if not logged in
      return

    try:
      if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
        auth.logout(request)
        del request.session['last_touch']
        return
    except KeyError:
      pass

    request.session['last_touch'] = datetime.now()



class Activity(object):
        def process_request(self,request):
                if request.META.has_key('HTTP_REFERER'):
                        referer = request.META['HTTP_REFERER']
                else:
                        referer = ''

                self.activity = UserActivity(
                                user = request.user,
                                session = request.session,
                                date = datetime.now(),
                                request_url = request.META['PATH_INFO'],
                                referer_url = referer,
                                client_address = request.META['REMOTE_ADDR'],
                                client_host = '',
                                browser_info = request.META['HTTP_USER_AGENT']
                                )

        def process_exception(self,request,exception):
                self.activity.error = exception
                self.activity.save()

        def process_response(self,request,response):
                self.activity.set_request_time()
                return response



        
