from django.conf.urls.defaults import *

from cal.controller import CalendarController
from cal.models import Event

## calendar view
urlpatterns = patterns('cal.views',
    (r'^view/.*$', 'view'),
    (r'^upd/.*$', 'updEvent'),
    (r'^add/.*$', 'addEvent'),
    (r'^del/.*$', 'delEvent'),
    (r'^.*$', 'view',{'header':'Organizator'}),
)

