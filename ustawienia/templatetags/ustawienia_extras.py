from django import template
from ustawienia.models import Wagi
from e_dziennik.models import Oceny,Nieobecnosci
from django.core.cache import cache
register = template.Library()





@register.filter
def waga(przedmiot_id,arg):
    w = Wagi.objects.filter(oceny__uczen=cache.get('uczen_id'),oceny__przedmiot=przedmiot_id)
    o = Oceny.objects.filter(uczen=cache.get('uczen_id'),przedmiot=przedmiot_id)
    try:return '%s<br>%s' % (w[arg].opis,o[arg].data_dodania)
    except:return ''

@register.filter
def kalendarz(dziecko,num):
    import cals
    n = Nieobecnosci.objects.filter(uczen=dziecko.id)
    myCal = cals.MonthlyCalendar(2008,num)
    myCal.offset = 2
    for i in n:
        if i.data.year == myCal.year and i.data.month == myCal.month:
            #myCal.specDays={'%s'%i.data.day:['#FF8C00','Zobacz szczegoly','ccccc']}
            myCal.specDays['%s'%i.data.day]=['#FFD700','Zobacz szczegoŁy','%s'%dziecko.id]
            #myCal.viewEvent(i.data.day, i.data.day, "#FFD700", "Kliknij, aby uzyskac wiecej informacji")
            
    return myCal.create()

@register.filter
def porownaj(num):
    if num ==4 or num==8:
        return True
    return False
@register.filter
def kolor(arg):
    kolory = {'s':'#C71585','-':'#FFD700','u':'#ADFF2F','n':'#FF6347','x':'#6495ED'}
    return kolory[arg]
    
