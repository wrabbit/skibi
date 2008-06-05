from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from e_dziennik.models import *
from ustawienia.models import *
from django.contrib.auth.models import Group,User,UserManager
from django.template import RequestContext
from django.core.cache import cache


def oceny_ucznia(request,uczen_id):
    cache.set('uczen_id',uczen_id,86400)
    liczba_kolumn = range(Ustawienia.objects.get(opis='oceny').kolumny)
    return render_to_response('oceny_ucznia.html',{'kolumny':liczba_kolumn,'header':'Oceny'},context_instance=RequestContext(request))        
    
   
def zapisz_potwierdzenie(request,uwaga_id,potwierdz):
    u = Uwagi.objects.get(id = uwaga_id)
    u.potwierdzenie = potwierdz
    u.save()
    return HttpResponse('ok')


def nieobecnosci_ucznia(request,header):
    months_num = range(1,13)
    return render_to_response('nb_ucznia.html',{'months_num':months_num,'header':header},context_instance=RequestContext(request))


def nieobecnosci_szczegoly(request,uczen_id):
    n = Nieobecnosci.objects.filter(uczen=uczen_id,data=request.GET['date']).order_by('wartosc').exclude(wartosc='x')
    header = 'Nieobecności ucznia w dniu %s' % '%s'%n[0].data
    return render_to_response('nb_ucznia_szczegoly.html',{'n':n,'header':header},context_instance=RequestContext(request))

def some_view(request):
    """testes view"""
    pass

