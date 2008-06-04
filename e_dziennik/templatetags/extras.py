from django import template
from django.core.cache import cache
from e_dziennik.models import *
from ustawienia.models import Ustawienia,Godziny
from django.contrib.auth.models import User,Group
from boxcomments.models import Comment
register = template.Library()
         
@register.filter        
def dolacz(value,arg,l=0):
    liczba_kolumn = Ustawienia.objects.get(opis='oceny').kolumny
    if arg =='sem': l = 3
    if arg =='pro': l = 2
    if arg =='sr': l = 1 
    return arg+'%s-%s' % (liczba_kolumn + l,value)

@register.filter 
def equal(value,arg=''):
    if value == 'uczniow':return True
    elif value =='przedmiotow':return False
    if int(value)==int(arg):return 'active'
    return False

@register.filter 
def tnij(value):
    return str(value)[:-3]

@register.filter 
def zawiera(value,arg):
    if arg in value:return True
    return False

    
@register.filter 
def leni(value,arg):
    return len(value) + int(arg)

@register.filter 
def pobierz_oceny(value,arg):
    przedmiot = cache.get('przedmiot')
    semestr = cache.get('semestr')
    o = Oceny.objects.filter(uczen = arg,pole=value,przedmiot=przedmiot,semestr=semestr)
    if len(o)>0:return o[0].ocena
    else:return ''
    
@register.filter   
def pobierz_info_oceny(value,arg):
    przedmiot = cache.get('przedmiot')
    o = Oceny.objects.filter(uczen = arg).filter(pole=value).filter(przedmiot=przedmiot)
    user = User.objects.get(id = o[0].user_id).get_full_name() 
    if len(o)>0:return 'Dodał: %s' % user + '<br>Data dodania: %s' % o[0].data_dodania
    else:return ''
    
@register.filter 
def pobierz_wagi(value,arg):
    semestr = cache.get('semestr')
    o = Oceny.objects.filter(pole=value,przedmiot=arg,semestr=semestr)
    if len(o)>0:return o[0].waga
    else:return ''

@register.filter 
def pobierz_koncowe(value,arg):
    liczba_kolumn = Ustawienia.objects.get(opis='oceny').kolumny
    nr_kolumny = value
    przedmiot = cache.get('przedmiot')
    semestr = cache.get('semestr')
    if (liczba_kolumn + 1 == nr_kolumny):
        sr = Srednie.objects.filter(pole=nr_kolumny,przedmiot=przedmiot,uczen = arg,semestr=semestr).values('srednia')
        if len(sr)>0:return sr[0]['srednia']
        else:return ''  
    else:
        o = Oceny.objects.filter(pole=nr_kolumny,przedmiot=przedmiot,uczen = arg,semestr=semestr)
        if len(o)>0:return o[0].ocena
        else:return ''  


@register.filter
def blokuj(user,klasa):
    przedmiot = cache.get('przedmiot')
    if Klasy.objects.filter(wychowawca = user.id,id = klasa) or Przedmioty.objects.filter(id = przedmiot.id,klasa = klasa,nauczyciel = user.id):
        return True
    return 'readonly'

@register.filter
def pobierz_lekcje(dzien,godzina):
    from string import capitalize
    klasa = cache.get('klasa')
    lekcja = PlanLekcji.objects.filter(godzina = godzina,dzien_tygodnia=dzien,klasa=klasa)
    if lekcja:
        return "<b>%s</b><br>%s<br>Sala: %s" % (capitalize(lekcja[0].przedmiot.nazwa),lekcja[0].przedmiot.nauczyciel.get_full_name(),
                                          lekcja[0].sala.numer)
    return '&nbsp'

@register.filter
def przetworz_plan(dzien,klasa):
    plan = PlanLekcji.objects.filter(klasa=klasa,dzien_tygodnia=dzien)
    if plan:return plan

@register.filter
def data(dzien):
    dzien = dzien.split('\n')[1]
    return dzien
    #return datetime.date(int(dzien[0]),int(dzien[1]),int(dzien[2]))


@register.filter
def pobierz_temat(godzina,dzien):
    temat = Tematy.objects.filter(klasa=cache.get('klasa'),godzina=godzina,data=dzien.split('\n')[1])
    if temat:return "<b>%s</b>" % temat[0].tresc
    return '&nbsp;'

@register.filter       
def sprawdz_typ(value):
    if value == 'Pozytywna':
        return 'pozytywna'
    return 'negatywna'

@register.filter       
def sprawdz_grupe(user):
    grupy = Group.objects.filter(user__id=user.id)
    for g in grupy:
        if g.name == 'Wychowawca' or g.name == 'Nauczyciel':return True
    return False

@register.filter
def pob(przedmiot_id,arg):
    o = Oceny.objects.filter(uczen=cache.get('uczen_id'),przedmiot=przedmiot_id)
    try:return o[arg].ocena
    except:return ''

import datetime
class DateRange(object):
    def __init__(self, start, stop, step=1, fmt="%H:%M"):
        assert step > 0
        self.start, self.stop = start, stop
        self.step, self.fmt = step, fmt
    def _inc(self):
        return self.start + datetime.timedelta(minutes=self.step)
    def __iter__(self):return self
    def next(self):
        if self.start >= self.stop:
            raise StopIteration
        else:
            curr = self.start
            self.start = self._inc()
            return curr.strftime(self.fmt)


weekdays = {0:'Poniedziałek',1:'Wtorek',2:'Środa',3:'Czwartek',4:'Piątek',5:'Sobota',6:'Niedziela'}
@register.filter
def sprawdz_plan(dzien,godzina):
    dzien = dzien
    plan = PlanLekcji.objects.filter(klasa = cache.get('klasa_id'),dzien_tygodnia = dzien,godzina=godzina.id)
    if plan:
        beg = str(godzina.poczatek)
        end = str(godzina.koniec)
        now=datetime.datetime.now()
        dates = list(DateRange(datetime.datetime(now.year, now.month,now.day,int(beg[:2]),int(beg[3:5]),0),
                           datetime.datetime(now.year, now.month,now.day,int(end[:2]),int(end[3:5]),0)))
        for m in dates:
            if m==now.strftime('%H:%M') and now.weekday()==dzien:
                return 'border:1px solid red'
        return True
    return False

@register.filter
def sprawdz_klase(user,klasa):
    przedmiot = cache.get('przedmiot')
    if Klasy.objects.filter(wychowawca = user.id).filter(id = klasa): return True
    if przedmiot is not None:
        if Przedmioty.objects.filter(id = przedmiot.id,klasa = klasa,nauczyciel = user.id):
            #cache.delete('przedmiot')
            return True
    return False
    '''    
    plan = PlanLekcji.objects.filter(klasa=klasa,godzina=cache.get('godzina'),dzien_tygodnia=cache.get('dzien_tyg'))
    if Przedmioty.objects.filter(id=plan[0].przedmiot.id,klasa = klasa,nauczyciel = user.id):
        return True
    '''
@register.filter
def pobierz_nieobecnosci(data,uczen_id):
    wpis_id = str(cache.get('godzina'))+str(uczen_id)+data.split('\n')[1].replace('-','')
    n = Nieobecnosci.objects.filter(id=wpis_id)
    if n:return n[0].wartosc
    return '&nbsp'

@register.filter
def pobierz_opiekuna(uczen_id):
    r = UczenProfile.objects.filter(uczen=uczen_id)
    if r:return r[0].rodzic.username
    return '-'


@register.filter
def cach(godzina):
    cache.set('godzina',godzina)
    return ''

@register.filter
def podziel(value):
    import os
    (filepath, filename) = os.path.split(value)
    return filename
@register.filter
def ilosc_msg(value):
    return len(Wiadomosci.objects.filter(user = value))
'''
@register.filter
def skrot(text):
    lista = text.split('\n')
    return '\n'.join(wiersz for wiersz in lista[0:5])+' ...'
'''
@register.filter
def skrot(text):
    l,k=[],[]
    for i in text:
        if i == '.':k.append(i)
        if len(k)<1:l.append(i)
    return ''.join(e for e in l) + '...'

@register.filter
def sql(id_news):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT if (LENGTH(news_text)>1000 ,SUBSTRING(news_text, 1, LOCATE(' ',news_text, 980)), news_text) as news_skrot FROM e_dziennik_aktualnosci WHERE id =%d" % id_news)
    row = cursor.fetchone()
    return row[0] + '...'
    
@register.filter
def wf(przedmiot):
    l = ['w-f', 'W-F','W-f', 'wychowawanie fizyczne', 'Wychowanie fizyczne','Wychowanie Fizyczne']
    if przedmiot.nazwa in l:
        return True
    return False



@register.filter
def create_calendar(year,month):
    import cals
    import calendar
    miesiac = calendar.monthcalendar(int(year),int(month))
    myCal = cals.MonthlyCalendar(year, month)
    for week in miesiac:
        for day in week:
            if day !=0:
                myCal.specDays['%s' % day]=['','Wybierz dzień','']
    return myCal.create()

@register.filter
def porownaj(arg,value):
    value = value.split('\n')[1]
    if arg==value:return True
    return False


@register.filter
def lencom(news):
    return Comment.objects.filter(appid=news).count()

@register.filter
def monit(uwaga):
    now = datetime.datetime.now()
    profil=UczenProfile.objects.filter(uczen=1)
    wiadomosc = u"""Uczeń %s otrzymal dnia %s uwage, ktora nie zostala potwierdzona. Prosze o potwierdzenie przeczytania.<br>
                Pozdrawiam %s""" % (uwaga.uczen.get_full_name(),uwaga.dodano,uwaga.wystawil.get_full_name())
    if not uwaga.potwierdzenie and uwaga.dodano + datetime.timedelta(days=3) < now and profil and not uwaga.monit:
        profil[0].rodzic.send_message(wiadomosc,uwaga.wystawil.get_full_name())
        uwaga.monit=1
        uwaga.save()
        return ''
    if uwaga.monit:
        return "<img src=/site_media/images/mt_email.png title='Powiadomienie zostało wysłane' align='middle'>"
    return ''

@register.filter
def del_img(arg):
    from django.conf import settings
    import os
    os.remove(settings.MEDIA_ROOT+'wykresy/wykres.png')
