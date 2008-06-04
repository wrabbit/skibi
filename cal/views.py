import datetime, calendar
import copy

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from controller import CalendarController
from django.template import RequestContext

def view(request,header):
    """Calendar view"""
    user = request.user
    date = datetime.datetime.now()
    default = dict(month=date.month, year=date.year, day=1, rowid=1,
            name="", desc="", when="")
    url = request.path

    p = getParams(request, default)
    year, month, day = p['year'], p['month'], p['day']

    # create calendar obj
    cal = CalendarController(user, day)
    cal.load(year, month)
    
    return render_to_response('calendar.html',dict(username=user.get_full_name(), cal=cal, url=url,header=header),context_instance=RequestContext(request))

def addEvent(request):
    """add event to calendar"""
    user = request.user
    default = dict(month=1, year=1, day=1, rowid=1, name="", desc="", when="")
    p = getParams(request, default)
    year, month, day = p['year'], p['month'], p['day']

    # create calendar obj
    cal = CalendarController(user, day)
    cal.load(year, month)

    # parpare data for adding Event
    whenDate = datetime.date(year, month, day)
    whenTime = datetime.time(*map(int, p['when'].strip().split(':')))
    when = datetime.datetime.combine(whenDate, whenTime)

    # adding Event
    cal.addEvent(day, p['name'], when, p['desc'])

    # show view with new result
    return redirect2view(request.path, year, month, day)


def delEvent(request):
    """delete event from calendar"""
    user = request.user
    default = dict(month=1, year=1, day=1, rowid=1, name="", desc="", when="")
    p = getParams(request, default)
    year, month, day = p['year'], p['month'], p['day']

    # create calendar obj
    cal = CalendarController(user, day)
    cal.load(year, month)

    # delete Event
    cal.delEvent(day, p['rowid'])

    # show view with new result
    return redirect2view(request.path, year, month, day)


def updEvent(request):
    """update selected event to calendar"""
    user = request.user
    default = dict(month=1, year=1, day=1, rowid=1, name="", desc="", when="")
    p = getParams(request, default)
    year, month, day = p['year'], p['month'], p['day']

    # create calendar obj
    cal = CalendarController(user, day)
    cal.load(year, month)

    # parpare data for adding Event
    whenDate = datetime.date(year, month, day)
    whenTime = datetime.time(*map(int, p['when'].strip().split(':')))
    when = datetime.datetime.combine(whenDate, whenTime)

    # update Event
    cal.updEvent(day, p['rowid'], p['name'], when, p['desc'])

    # show view with new result
    return redirect2view(request.path, year, month, day)


## helper function
def getParams(request, default):
    """get parameter (case insensitive for key) (support both get and post)
        param is updated as side effect (for now)"""
    paramKeys = ['year', 'month', 'day', 'rowid', 'name', 'desc', 'when']
    paramFunc =  [int, int, int, int, str, str, str ]
    paramDef = dict(zip(paramKeys, paramFunc))

    inputDict = getattr(request, request.method, {})
    result = copy.deepcopy(default)
    for k in inputDict:
        kl = k.lower()
        if kl in default and kl in paramDef:
            try:
                result[kl] = paramDef[kl](getattr(request, request.method)[k])
            except KeyError:
                pass
    return result


def upOneLevelURL(url):
    """eg1:  upOneLevelURL('http://aaa/bbb/ccc') == 'http://aaa/bbb/'
       eg2:  upOneLevelURL('http://aaa/bbb/ccc/') == 'http://aaa/bbb/'
       eg3:  upOneLevelURL('http://aaa/bbb/ccc/?xyz') == 'http://aaa/bbb/'
       eg4:  upOneLevelURL('http://aaa/bbb/ccc?xyz') == 'http://aaa/bbb/'
    """
    sep = '/'
    result = url.split('?')[0]
    if result[-1] == sep:
        result = result[:-1].rsplit(sep, 1)[0]
    else:
        result = result.rsplit(sep, 1)[0]
    return result + sep


def redirect2view(url, year, month, day):
    url = upOneLevelURL(url)
    qstr = '?year=%d&month=%d&day=%d' % (year, month, day)
    url += qstr
    return HttpResponseRedirect(url)

