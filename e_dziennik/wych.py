from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from e_dziennik.models import *
from ustawienia.models import *
from django.contrib.auth.models import Group,User,UserManager
from django.template import RequestContext
import django

slownik = {'Lista uczniow':Uczniowie_tmp,'Lista przedmiotow':Przedmioty,'User':User,'Plan':PlanLekcji}
def wyswietl(request,klasa_id,klucz):     # dot. uczniow i przedmiotow
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        model = slownik[klucz]
	lista = model.objects.filter(klasa=klasa_id)
	if len(lista) == 0:info = klucz[6:]
	else: info=''
	return render_to_response('base_tresc.html',
        {'_'.join(klucz.split()):lista,
         'header':klucz,
         'brak_danych':info},context_instance=RequestContext(request))
                        
from django.newforms import form_for_model
from django.core.cache import cache
def wyswietl_oceny(request,klasa_id,liczba_kolumn=None):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        try:
                przedmioty = Przedmioty.objects.filter(klasa=klasa_id)
                przedmiot = przedmioty[0]
                semestry = Semestry.objects.all()
                semestr = semestry[0]
                wagi = Wagi.objects.all()
                lista_uczniow = Uczniowie_tmp.objects.filter(klasa = klasa_id)
                if request.GET.has_key('przedmiot') or request.POST.has_key('przedmiot'):
                        przedmiot = Przedmioty.objects.get(id=request.REQUEST['przedmiot'],klasa=klasa_id)
                        grupy = Grupy_jezykowe.objects.all()
                        lang = przedmiot.nazwa.split()
                        if len(lang)>1:
                                for g in grupy:
                                        if g.nazwa== lang[1]:lista_uczniow = Uczniowie_tmp.objects.filter(klasa=klasa_id,grupa=g.id)
                if request.GET.has_key('semestr')  or request.POST.has_key('semestr'):
                        semestr = Semestry.objects.get(id=request.REQUEST['semestr'])
                if request.POST.has_key('plec'):
                        lista_uczniow=Uczniowie_tmp.objects.filter(klasa=klasa_id,plec=request.REQUEST['plec'])
                
                        
                cache.set('przedmiot', przedmiot,86400)
                cache.set('semestr',semestr,86400)
                liczba_kolumn = range(Ustawienia.objects.get(opis='oceny').kolumny)
                return render_to_response('oceny.html',
                                          {'przedmioty':przedmioty,'kolumny':liczba_kolumn,'uczniowie':lista_uczniow,'przedmiot':przedmiot,
                                           'semestry':semestry,'semestr':semestr,'wagi':wagi,'header':'Oceny'},context_instance=RequestContext(request))
        except:return render_to_response('brak_danych.html',{'header':'Oceny'},context_instance=RequestContext(request))



def wstaw_oceny(request,klasa_id,przedmiot_id,semestr_id,l=[]):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        if request.method == 'POST':
                new_data = request.POST.copy()
                for k in new_data.keys():
                        if 'w' in k:l.append(k.strip('w'))
                        if 'w' not in k:
                                wpis_id = int('%s%s%s'%(przedmiot_id,''.join(e for e in k.strip('sem').strip('pro').strip('sr').split('-')),semestr_id)) 
                                for e in [Oceny]:
                                        exist = e.objects.filter(id = wpis_id)
                                        if exist and new_data[k]=='':exist.delete()
                                        if exist:exist=exist[0].ocena
                                        else:exist=''                
                                pole = k.split('-')[0].strip('sem').strip('pro').strip('sr')
                                uczen_id = k.split('-')[1]
                                if new_data[k]!='' and str(new_data[k])!= str(exist):
                                        grupa = sprawdz_grupe(request,klasa_id,przedmiot_id)
                                        if request.user.has_perm('e_dziennik.add_oceny') and grupa is 'wych' or grupa is 'nau':
                                                if 'sr' not in k:ocena_id = Wartosci_ocen.objects.get(nazwa=new_data[k]).id
                                                if 'pro' in k:
                                                        waga=0
                                                        waga_id = Wagi.objects.get(waga = waga).id
                                                        new_ocena = Oceny(id=wpis_id,klasa_id=klasa_id,przedmiot_id=przedmiot_id,
                                                                  ocena_id=ocena_id,uczen_id=uczen_id,waga_id=waga_id,pole=pole,
                                                                  semestr_id=semestr_id,user_id = request.user.id)
                                                        new_ocena.save()
                                                        profil=UczenProfile.objects.filter(uczen=uczen_id)
                                                        if new_data[k]=='1' and profil:
                                                                rodzic = User.objects.get(uczenprofile__uczen=uczen_id)
                                                                wiadomosc = u"""Uczeń %s jest zagrożony
                                                                         oceną niedostateczną z przedmiotu %s.
                                                                         Proszę o kontakt.""" % (profil[0].uczen,Przedmioty.objects.get(id=przedmiot_id)) 
                                                                profil[0].rodzic.send_message(wiadomosc,request.user.get_full_name())             
                                                if 'sr' in k:
                                                        new_srednia = Srednie(id=wpis_id,klasa_id=klasa_id,przedmiot_id=przedmiot_id,
                                                                      semestr_id=semestr_id,srednia=new_data[k],uczen_id=uczen_id,pole=pole)
                                                        new_srednia.save()
                                                for j in l:
                                                        if pole == j:
                                                                waga=new_data['w%s' % j]
                                                                if not len(waga):waga = 1
                                                                waga_id = Wagi.objects.get(waga = waga).id
                                                                new_ocena = Oceny(id=wpis_id,klasa_id=klasa_id,przedmiot_id=przedmiot_id,
                                                                          ocena_id=ocena_id,uczen_id=uczen_id,waga_id=waga_id,pole=pole,
                                                                          semestr_id=semestr_id,user_id = request.user.id)
                                                                new_ocena.save()
                return HttpResponseRedirect('/'+klasa_id+'/Oceny/?semestr='+semestr_id+'&przedmiot='+przedmiot_id)

from django import newforms as forms
weekdays = {0:'Poniedziałek',1:'Wtorek',2:'Środa',3:'Czwartek',4:'Piątek',5:'Sobota',6:'Niedziela'}

def wyswietl_plan(request,klasa_id):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        godziny = Godziny.objects.all()
        cache.set('klasa',klasa_id,86400)
        return render_to_response('plan.html',{'godziny':godziny,'weekdays':weekdays,'header':'Plan lekcji'},
                                               context_instance=RequestContext(request))

class PlanForm(forms.Form):
        przedmiot = forms.CharField(max_length=30)
        sala = forms.ModelChoiceField(queryset=Sale.objects.all())
        

def dodaj_lekcje(request,klasa_id,godzina_id,dzien,edit=None,data=None):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        query = Przedmioty.objects.filter(klasa=klasa_id) #przedmioty danej klasy
        if request.POST:
                form = PlanForm(request.POST)
                form.fields['przedmiot'] = forms.ModelChoiceField(queryset = query)
                if form.is_valid():
                        new_data = request.POST.copy()
                        wpis_id = dzien+klasa_id+godzina_id
                        new_lekcja = PlanLekcji(id=wpis_id,klasa_id = klasa_id,przedmiot_id=new_data['przedmiot'],godzina_id=godzina_id,
                                                dzien_tygodnia=dzien,sala_id=new_data['sala'])
                        new_lekcja.save()
                        return HttpResponseRedirect('/'+klasa_id+'/Plan/')
                else:
                        
                        return render_to_response('plan_add.html',{'f':form},context_instance=RequestContext(request))
        else:
                exist = PlanLekcji.objects.filter(klasa = klasa_id,dzien_tygodnia=dzien,godzina=godzina_id)
                if exist:data = {'sala':exist[0].sala_id,'przedmiot':exist[0].przedmiot_id}
                form = PlanForm(data)
                form.fields['przedmiot'] = forms.ModelChoiceField(queryset = query)
                return render_to_response('plan_add.html',{'f':form,'exist':exist},context_instance=RequestContext(request))

TYPES = (('Pozytywna', 'Pozytywna'), ('Negatywna', 'Negatywna'))
def dodaj_uwage(request,uczen_id):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        if not request.user.has_perm('e_dziennik.add_uwagi'): return HttpResponse(perm_denied(request,klasa_id,model='Uwagi'))  
        uczen = Uczniowie_tmp.objects.get(id=uczen_id)
        UwagaForm = form_for_model(Uwagi)
        form = UwagaForm()
        if request.POST:
                new_data = request.POST.copy()
                new_data['uczen']=uczen_id
                new_data['wystawil']=request.user.id
                form = UwagaForm(new_data)
                if form.is_valid():
                        new_msg=form.save()
                        return HttpResponseRedirect('/'+uczen_id+'/sprawdz/uwagi/')
                else:
                        form.fields['typ']=forms.ChoiceField(choices=TYPES,widget=forms.RadioSelect)
                        return render_to_response('uwagi_form.html',{'f':form,'uczen':uczen},context_instance=RequestContext(request))
                        
        else:
                form.fields['typ']=forms.ChoiceField(choices=TYPES,widget=forms.RadioSelect)
                return render_to_response('uwagi_form.html',{'f':form,'uczen':uczen},context_instance=RequestContext(request))

from django import oldforms

def edytuj_uwage(request,uwaga_id,uczen_id):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        if not request.user.has_perm('e_dziennik.change_uwagi'): return HttpResponse(perm_denied(request,model='Uwagi')) 
        uczen = Uczniowie_tmp.objects.get(id=uczen_id)
        manipulator = Uwagi.ChangeManipulator(uwaga_id)
        rekord = manipulator.original_object
        if request.POST:
                new_data = request.POST.copy()
                new_data['uczen']=uczen_id
                new_data['wystawil']=request.user.id
                errors = manipulator.get_validation_errors(new_data)
                if not errors:
                        manipulator.do_html2python(new_data)
                        manipulator.save(new_data)
                        return HttpResponseRedirect('/'+uczen_id+'/sprawdz/uwagi/')
        else:
                errors = {}
                new_data = rekord.__dict__
        form = oldforms.FormWrapper(manipulator, new_data, errors)
        return render_to_response('uwagi_form.html',{'f':form,'uczen':uczen},context_instance=RequestContext(request))

def usun_uwage(request,uwaga_id,uczen_id):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        if not request.user.has_perm('e_dziennik.delete_uwagi'): return HttpResponse(perm_denied(request,model='Uwagi')) 
        rekord = Uwagi.objects.filter(id = uwaga_id)
        rekord.delete()
        return HttpResponseRedirect('/'+uczen_id+'/sprawdz/uwagi/')

def sprawdz_grupe(request,klasa_id,przedmiot_id=None):
        if Klasy.objects.filter(wychowawca = request.user.id).filter(id = klasa_id):
                return 'wych'
        if Przedmioty.objects.filter(nauczyciel = request.user.id).filter(klasa = klasa_id).filter(id=przedmiot_id):
                return 'nau'
def grupy(action,user_id,group):
        tmp = User.objects.get(id = user_id)
        if action=='add':tmp.groups.add(group)
        else: tmp.groups.remove(group)
        tmp.save()

def skaluj_obraz(path):
        import Image
        im = Image.open(path)
        (filepath, filename) = os.path.split(path)
        im.thumbnail((128, 128))
        im.save(settings.MEDIA_ROOT+'files/photos/mini/'+filename, "JPEG")


def dodaj(request,klasa_id,klucz):      # dot. uczniow i przedmiotow
    if not request.user.is_authenticated():return HttpResponseRedirect('/')
    grupa = sprawdz_grupe(request,klasa_id)
    if request.user.has_perm('e_dziennik.add_uczniowie_tmp') and grupa is 'wych':
            model = slownik[klucz]
            manipulator = model.AddManipulator()
            if request.POST:
                    # dane wyslane POSTem, kopiujemy je i chcemy tworzyc nowy obiekt
                    new_data = request.POST.copy()
                    new_data.update(request.FILES)
                    new_data['klasa']=klasa_id
                    # Sprawdzamy bledy;jezeli beda formularz przeladuje sie zachowujac dane,bo sa one w new_data
                    errors = manipulator.get_validation_errors(new_data)
                    if not errors:
                            # Brak bledow czyli zapisujemy!
                            manipulator.do_html2python(new_data)
                            new_r = manipulator.save(new_data)
                            if request.FILES:skaluj_obraz(new_r.get_photo_filename())
                            # wyswietl dane ucznia,aby dodac rodzica
                            if new_data.has_key('imie'):
                                    return render_to_response(
                                            'base_tresc.html',{'uczen':new_r,'tytul':'Uczeń został dodany'},
                                            context_instance=RequestContext(request))
                            else:
                                    grupy('add',new_data['nauczyciel'],2)#2->grupa:Nauczyciel
                                    return HttpResponseRedirect('/'+klasa_id+'/'+ klucz + '/')
            else:
                    # Brak danych POST, chcemy czysty formularz
                    errors = new_data = {}
                    # Tworzymy wrappera, szablon i reszte
            form = oldforms.FormWrapper(manipulator,new_data,errors)
            klucz = ''.join(klucz.split())
            return render_to_response('forms_wych.html',
                                      {klucz: form,'tytul':'Dodaj'},context_instance=RequestContext(request))
        
    else:
            #raise Http404
            return HttpResponseRedirect('/perm/'+klucz+'/')          

	
def edytuj(request,klasa_id,r_id,klucz,brak_r=None):  #dot. uczniow i przedmiotow
    if not request.user.is_authenticated():
            return HttpResponseRedirect('/')
    # sprawdz czy zdefiniowano rodzica
    grupa = sprawdz_grupe(request,klasa_id)
    znajdz = UczenProfile.objects.filter(uczen= r_id)
    model = slownik[klucz] 
    if  klucz == 'Lista uczniow' and len(znajdz) == 0: brak_r=True          
    # pobierz id rodzica z tabeli User na pdst. id ucznia z tabeli Uczniowie
    rodzic = User.objects.filter(uczenprofile__uczen=r_id)
    # jezeli rekord o podanym id istnieje to stworz ChangeManipulator
    try:
            manipulator = model.ChangeManipulator(r_id)
    except model.DoesNotExist:
            raise Http404
    # Pobieramy oryginalne dane
    rekord = manipulator.original_object
    if request.POST:
            new_data = request.POST.copy()
            new_data.update(request.FILES)
            new_data['klasa']=klasa_id
            for r in rodzic:new_data['rodzic']=r.id
            errors = manipulator.get_validation_errors(new_data)
            if not errors:
                    manipulator.do_html2python(new_data)
                    if request.user.has_perm('e_dziennik.change_przedmioty') and request.user.has_perm('e_dziennik.change_uczniowie_tmp') and grupa == 'wych':
                            new_r=manipulator.save(new_data)
                            if request.FILES:skaluj_obraz(new_r.get_photo_filename())
                            return HttpResponseRedirect('/'+klasa_id+'/'+klucz + '/')
                    else:
                            raise Http404
    else:
            errors = {}
            # Dzieki temu formularz poprawnie rozpozna dane dla kazdego pola
            new_data = rekord.__dict__

    form = oldforms.FormWrapper(manipulator, new_data, errors)
    klucz = ''.join(klucz.split())
    return render_to_response('forms_wych.html',
    {klucz: form,'rekord': rekord,'tytul': 'Edycja','del':'yes','r_id':r_id,'brak_r':brak_r,'rodzic':rodzic,
     },context_instance=RequestContext(request))


def usun(request,klasa_id,r_id,klucz):        # dot. uczniow,przedmiotow,rodzicow,planu_lekcji
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        grupa = sprawdz_grupe(request,klasa_id)
        if request.user.has_perm('e_dziennik.delete_uczniowie_tmp') and  request.user.has_perm('e_dziennik.delete_przedmioty') and grupa == 'wych':
                model = slownik[klucz]
                try:
                        rodzic = User.objects.get(uczenprofile__uczen=r_id)
                        rodzic.delete()
                finally:
                        rekord = model.objects.filter(id = r_id)
                        rekord.delete()
                        if model==User:klucz='Lista uczniow'
                        return HttpResponseRedirect('/'+klasa_id+ '/'+klucz+'/')
        else:
                raise Http404
                #return HttpResponseRedirect('/perm/'+klucz+'/')   


class UserExist(forms.Form):
        rodzic = forms.ModelChoiceField(queryset=User.objects.all())      

from django.core.mail import send_mail

def dodaj_rodzica(request,klasa_id,klucz,uczen_id,rodzic=None):
        '''Tworzy konto rodzica w modelu User,oraz konto ucznia w modelu Uczniowie'''
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        manipulator = User.AddManipulator()
        form1 = UserExist()
        if request.POST:
                new_data = request.POST.copy()
                if new_data.has_key('rodzic'): # wybierz istniejace konto
                        grupy('add',new_data['rodzic'],4) # 4-Rodzice
                        rodzic = new_data['rodzic']
                else:
                        new_data['groups']=4
                        errors = manipulator.get_validation_errors(new_data)

                        if not errors:
                                from django.core.mail import EmailMultiAlternatives
                                #Wyslanie e-maila z danymi do opiekuna
                                subject = 'Wiadomość z systemu e-dziennik.'
                                from_email = request.user.email
                                to = new_data['email']
                                text_content = 'Witaj' + new_data['first_name'] + new_data['last_name'] + 'Twoje dane w systemie e-dziennik: login:' + new_data['username'] + 'password:' + new_data['password']
                                html_content = 'Witaj<b>' + ' ' +new_data['first_name'] + ' ' + new_data['last_name'] + '</b><br><br>Twoje dane w systemie e-dziennik:<br><br>login:<b>' + ' ' + new_data['username'] + '</b><br>password:<b>' + ' ' + new_data['password'] + '</b>'
                                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                                msg.attach_alternative(html_content, "text/html")
                                msg.send()
                                u = User()
                                new_data['password'] = u.set_password(new_data['password'])
                                manipulator.do_html2python(new_data)
                                new_r = manipulator.save(new_data)
                                r = User.objects.get(username = new_data['username'])
                                rodzic = r.id
                                u = Uczniowie_tmp.objects.get(id = uczen_id)
                                #Profil
                                new_profile = UczenProfile(uczen=u,rodzic_id=rodzic,klasa=u.klasa)
                                new_profile.save()
                                return render_to_response('info.html',{'tresc':'''Na podany przy rejestracji e-mail została
                                        wysłana wiadomość z loginem i hasłem do systemu''',
                                        'back':'/'+klasa_id+'/Lista uczniow/'},context_instance=RequestContext(request))
                                #return HttpResponseRedirect('/'+klasa_id+'/Lista uczniow/')                  
        else:  
                errors = new_data = {}
        form = oldforms.FormWrapper(manipulator,new_data,errors)
        klucz = ''.join(klucz.split())
        u = Uczniowie_tmp.objects.get(id=uczen_id)
        full_name = u.get_full_name()
        return render_to_response('forms_wych.html',{klucz: form,'user_exist':form1,'tytul': 'Dodaj','header': 'Dodaj opiekuna','klasa':klasa_id,
                                                     'dane_ucznia':full_name,},context_instance=RequestContext(request))


def edytuj_rodzica(request,klasa_id,rod_id,klucz,r_id):
    if not request.user.is_authenticated():return HttpResponseRedirect('/')
    #model = slownik[klucz]
    try:
            manipulator = User.ChangeManipulator(rod_id)
    except User.DoesNotExist:
            raise Http404
    rekord = manipulator.original_object
    x = UserManager()
    pas = x.make_random_password()
    from django.contrib.auth.models import get_hexdigest
    #passs = get_hexdigest('sha1', '', pas)
    if request.POST:
            new_data = request.POST.copy()
            if new_data['password']=='':new_data['password']=rekord.password
            else:
                    u = User()
                    new_data['password'] = u.set_password(new_data['password'])
                    
            new_data['groups']=4
            
            errors = manipulator.get_validation_errors(new_data)
            if not errors:
                    
                    manipulator.do_html2python(new_data)
                    manipulator.save(new_data)
                    return HttpResponseRedirect('/'+klasa_id+ '/Lista uczniow/')           
    else:
            errors = {}
            new_data = rekord.__dict__
            

    form = oldforms.FormWrapper(manipulator, new_data, errors)
    u = Uczniowie_tmp.objects.get(id=r_id)
    full_name = u.get_full_name()
    return render_to_response('forms_wych.html',
    {klucz: form,'rekord': rekord,'tytul': 'Edycja','header':'Edycja ucznia','del':'yes','rod_id':rod_id,'dane_ucznia':full_name},
                              context_instance=RequestContext(request))


'''
from django.shortcuts import get_object_or_404
from e_dziennik.models import UserProfile
from e_dziennik.forms import RegistrationForm
import random, sha

def register(request):
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response('reg/register.html', {'has_account': True})
    manipulator = RegistrationForm()
    if request.POST:
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            # Save the user                                                                                                                                                 
            manipulator.do_html2python(new_data)
            new_user = manipulator.save(new_data)
            
            # Build the activation key for their account                                                                                                                    
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+new_user.username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            
            # Create and save their profile                                                                                                                                 
            new_profile = UserProfile(user=new_user,
                                      activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()
            
            # Send an email with the confirmation link                                                                                                                      
            email_subject = 'Potwierdzenie utworzenia konta na e-dziennik.one.pl'
            email_body ="""
Witaj, %s, dziekujemy za rejestracje w systemie                                                                                                      
e-dziennik.one.pl !\n\nAby aktywowac swoje konto kliknij ponizszy link w ciagu 48 godzin:                                                                                              
\n\nhttp://127.0.0.1:8080/accounts/confirm/%s"""% (new_user.username,new_profile.activation_key)
            send_mail(email_subject,
                      email_body,
                      'admin@e-dziennik.one.pl',
                      [new_user.email])
            
            return render_to_response('reg/register.html', {'created': True})
    else:
        errors = new_data = {}
    form = oldforms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('reg/register.html', {'form': form})


def confirm(request, activation_key):
    if request.user.is_authenticated():
        return render_to_response('reg/confirm.html', {'has_account': True})
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
    if user_profile.key_expires < datetime.datetime.today():
        return render_to_response('reg/confirm.html', {'expired': True})
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    return render_to_response('reg/confirm.html', {'success': True})
'''
from django.conf import settings
import PyXLReader
from PyXLReader import PyXLReader

def dane_z_pliku(request,klasa_id):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        DaneForm = form_for_model(DaneUczniow)
        form = DaneForm()
        if request.POST or request.method == "POST":
                
                new_data = request.POST.copy()
                new_data.update(request.FILES)
                form = DaneForm(new_data)
                if form.is_valid() and new_data['plik']['filename'].split('.')[-1] == 'xls':
                        dirname = settings.MEDIA_ROOT+'files/lista uczniow/'
                        for f in os.listdir(dirname):
                                if new_data['plik']['filename']==f:
                                        os.remove(dirname+f)
                        t = DaneUczniow()
                        t.opis = new_data['opis']
                        t.save_plik_file(new_data['plik']['filename'],new_data['plik']['content'])
                        Uczniowie_tmp.objects.filter(klasa=klasa_id).delete()
                        xlsfile=PyXLReader()
                        try:
                                xlsfile.read(dirname+new_data['plik']['filename'])
                                l = []
                                for sheetnumber, sheetdata in xlsfile.sheets.items()[:1]:
                                        for row,cols in sheetdata['cells'].items():
                                                numer = cols[1]
                                                imie = cols[2]
                                                nazwisko = cols[3]
                                                grupa = Grupy_jezykowe.objects.get(nazwa=cols[4]).id
                                                u = Uczniowie_tmp(numer=numer,imie=imie,nazwisko=nazwisko,klasa_id=klasa_id,grupa_id=grupa)
                                                u.save()
                                        return HttpResponseRedirect('/'+klasa_id+'/Lista uczniow/')
                        except:
                                return HttpResponse('Niepoprawny format pliku')
                else: return render_to_response('dane_uczniow2.html',{'f':form},context_instance=RequestContext(request))
        else: return render_to_response('dane_uczniow2.html',{'f':form},context_instance=RequestContext(request))

import calendar

def pobierz_tydzien(year=None,month=None,day=None):
        tydzien = []
        if year==None:
                now = datetime.date.today()
                rok = now.year
                miesiac = now.month
                dzien=now.day
        else:
                rok=int(year)
                miesiac=int(month)
                dzien=int(day)
                
        miesiac_list = calendar.monthcalendar(int(rok),int(miesiac))
        for week in miesiac_list:
                if dzien in week:
                        for d in range(len(week)):
                                s = {}
                                s[d] = '%s\n%s-%s-%s' % (weekdays[d],rok,miesiac,week[d])
                                tydzien.append(s)
                                if week[d]==0:tydzien.remove(s)
        return tydzien

import datetime
def wyswietl_nieobecnosci(request,klasa_id,year=None,month=None,day=None,date=None):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        if request.GET:
                date = request.GET['date']
                data = request.GET['date'].split('-')
                year = data[0]
                month=data[1]
                day = data[2]
        g = Godziny.objects.all()
        cache.set('klasa_id',klasa_id)
        return render_to_response('nb.html',{'header':'Nieobecności',
                                                       'data':date,
                                                       'tydzien':pobierz_tydzien(year,month,day),
                                                       'godziny':g},context_instance=RequestContext(request))
       
def dodaj_nieobecnosci(request,klasa_id,j=[],data=None):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        new_data = request.POST.copy()
        for key,value in new_data.items():
                l = key.split('\n')
                godzina_id = l[0].split('-')[0]
                uczen_id = l[0].split('-')[1]
                data=datetime.date(int(l[1].split('-')[0]),int(l[1].split('-')[1]),int(l[1].split('-')[2]))
                wpis_id = godzina_id+uczen_id+l[1].replace('-','')
                exist=Nieobecnosci.objects.filter(id=wpis_id)
                if exist:exists=exist[0].wartosc
                else:exists=''
                if value.strip() and exists!=value.strip():
                        if value.strip()=='n':
                                #wyslanie sms-a
                                import sms_orangembox
                                from sms_orangembox import *
                                profil = UczenProfile.objects.filter(uczen = uczen_id)
                                if profil:
                                        phone = profil[0].rodzic.mobile_phone
                                        if phone:
                                                message='Uczen %s ma nieobecnosc nieusprawiedliwiona dnia %s na %s godzinie lekcyjnej' % (profil[0].uczen,data,godzina_id)
                                                sendsms(request.user.get_full_name(),str(phone),message)
                                        
                        new_nieobecnosc = Nieobecnosci(id = wpis_id,wartosc = value,uczen_id = uczen_id,wstawil_id=request.user.id,
                                                       godzina_id=godzina_id,data = data)
                        new_nieobecnosc.save()
                if exist and value=='':exist[0].delete()
        if request.GET:return HttpResponseRedirect('/'+klasa_id+'/Nieobecnosci/?date='+request.GET['date'])
        return HttpResponseRedirect('/'+klasa_id+'/Nieobecnosci/')




from e_dziennik.models import *
from pychartdir import *

def wyswietl_raporty(request,klasa_id,typ,podtyp):
        if typ=='szkola':
                k = Klasy.objects.all()
                #N = len(k)
                sm,sp,nn,nu=[],[],[],[]
                klasy = [str(i) for i in k]
                for i in k:
                        suma = Nieobecnosci.objects.filter(uczen__klasa = i.id)
                        sm.append(suma.count())
                        sp.append(suma.filter(wartosc ='s').count())
                        nn.append(suma.filter(wartosc ='n').count())
                        nu.append(suma.filter(wartosc ='u').count())
                data0,data1,data2,data3 = sp,nu,nn,sm
                labels = klasy
                c = XYChart(540, 375)
                c.addTitle("Zestawienie nieobecności w klasach", "timesbi.ttf", 18)
                c.setPlotArea(50, 55, 440, 280, c.linearGradientColor(0, 55, 0, 335, 0xffdddd,0x880000), -1, 0xffffff, 0xffffff)
                c.addLegend(50, 25, 0, "arialbd.ttf", 10).setBackground(Transparent)
                c.xAxis().setLabels(labels)
                c.xAxis().setTickOffset(0.5)
                c.xAxis().setLabelStyle("arialbd.ttf", 8)
                c.yAxis().setLabelStyle("arialbd.ttf", 8)
                c.xAxis().setWidth(2)
                c.yAxis().setWidth(2)
                #c.yAxis().setTitle("Throughput (MBytes Per Hour)")
                layer = c.addBarLayer2(Side, 4)
                if podtyp=='sn':
                        layer.addDataSet(data0, 0xffff00, "spóźnienia")
                        layer.addDataSet(data1, 0x00ff00, "nieob. uspr.")
                        layer.addDataSet(data2, 0x9999ff, "nieob. nieuspr.")
                if podtyp=='on':
                        layer.addDataSet(data3, 0x1E90FF, "suma nieobecności")
                layer.setBorderColor(Transparent, softLighting(Top))
                layer.setBarGap(0.2, TouchBar)
        if typ=='klasa':
                oceny = Oceny.objects.filter(klasa=klasa_id)
                bdb = len(oceny.filter(ocena__nazwa='5'))
                db = len(oceny.filter(ocena__nazwa='4'))
                dst = len(oceny.filter(ocena__nazwa='3'))
                dop = len(oceny.filter(ocena__nazwa='2'))
                ndst = len(oceny.filter(ocena__nazwa='1'))
                cel = len(oceny.filter(ocena__nazwa='6'))
                data = [bdb,db,dst,dop,ndst,cel]
                depths = [30, 20, 10, 10]
                labels = ["bdb (%s)"%bdb,"db (%s)"%db, "dst(%s)"%dst, "dop(%s)"%dop,
                          "ndst(%s)"%ndst,"cel(%s)"%cel]
                #icons = ["sun.png", "cloud.png", "rain.png", "snowy.png"]
                c = PieChart(400, 310, metalColor(0xccccff, 0), 0x000000, 1)
                c.setRoundedFrame()
                c.setPieSize(200, 180, 100)
                c.addTitle("Procentowy rozkład wszystkich ocen", "timesbi.ttf", 15).setBackground(0xccccff, 0x000000, glassEffect())
                c.setData(data, labels)
                #c.addExtraField(icons)
                c.setLabelFormat("<*block,valign=absmiddle*><*img={field0}*> <*block*>{label}\n{percent}%<*/*><*/*>")
                c.set3D2(depths)
                c.setStartAngle(225)
        c.makeChart(settings.MEDIA_ROOT+'wykresy/wykres.png')
        
        return render_to_response('wykresy.html',{'header':'Raporty'},context_instance=RequestContext(request))


import sys
from PyRTF import *

def kartki(klasa_id):
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)
    u = Uczniowie_tmp.objects.filter(klasa=klasa_id)
    p = Przedmioty.objects.filter(klasa=klasa_id)
    for i in u:
        nb = Nieobecnosci.objects.filter(uczen=i.id,wartosc='n').count()
        
        s,l={},[]
        para_props = ParagraphPS()
        para_props.SetPageBreakBefore( True )
        par = Paragraph(para_props)
        klasa = Klasy.objects.get(id=klasa_id)
        par.append(TEXT(str(i), font=ss.Fonts.TimesNewRoman,bold=True,underline=True,size=23 ))
        par.append(TEXT("- uczen klasy "+str(klasa),font=ss.Fonts.TimesNewRoman,size=20))
        section.append(par)
        section.append('')
        for j in p:
            try:
                    sr_p=Srednie.objects.get(uczen=i.id,przedmiot=j.id).srednia
                    l.append(sr_p)
            except:
                    sr_p='0.0'
            oceny=[]
            o = Oceny.objects.filter(klasa=klasa_id,uczen=i.id,przedmiot=j.id)
            par=Paragraph()
            par.append(TEXT( str(j), font=ss.Fonts.TimesNewRoman,bold=True,size=23 ))
            section.append(par)
            
            for e in o:
                if i.id == e.uczen.id and j.id==e.przedmiot.id:
                    oceny.append(str(e.ocena))
            if oceny:
                para_props = ParagraphPS( tabs = [ TabPS( width=TabPS.DEFAULT_WIDTH     ),
									   TabPS( width=TabPS.DEFAULT_WIDTH * 2 ),
									   TabPS( width=TabPS.DEFAULT_WIDTH     ) ] )
                par = Paragraph( ss.ParagraphStyles.Normal, para_props )
                par.append( ','.join(n for n in oceny), TAB,TAB,TEXT('(%s)' % sr_p,italic=True))
                section.append( par )
            else:
                section.append('------')
        section.append('')
        par=Paragraph()
        par.append(TEXT('Liczba godzin nieuspr. : %s' % nb,font=ss.Fonts.TimesNewRoman,size=23))
        section.append(par)
        par=Paragraph()
        suma = 0.0
        for i in l:
                suma = suma + i
        if l:sr_u = suma / len(l)
        else:sr_u=0.0
        par.append(TEXT('SREDNIA UCZNIA: %0.2f' % sr_u,font=ss.Fonts.TimesNewRoman,bold=True,size=21))
        section.append(par)
        section.append('')
        section.append('........................')
        par=Paragraph()
        par.append(TEXT('podpis wychowawcy', font=ss.Fonts.TimesNewRoman,size=20,italic=True ))
        section.append(par)
    return doc

def zapisz_kartki(request,klasa_id):
        #return HttpResponse(settings.MEDIA_ROOT+'files/kartki/kartki_%s.doc' % datetime.date.today())
	DR = Renderer()
	doc1 = kartki(klasa_id)
	
	DR.Write( doc1,file( settings.MEDIA_ROOT+'files/kartki/kartki_%s.doc' % datetime.date.today(),'w' ) )
	return HttpResponseRedirect('/site_media/files/kartki/kartki_%s.doc' % datetime.date.today())


def filtruj_plec(request,klasa_id,plec):
        u = Uczniowie_tmp.objects.get(id=37)
        u.numer='333'
        u.save()
        return HttpResponseRedirect('/')
        return HttpResponse('ok')

def wyswietl_tematy(request,klasa_id,id='',year=None,month=None,day=None,date=None):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        if request.GET:
                date = request.GET['date']
                data = request.GET['date'].split('-')
                year = data[0]
                month=data[1]
                day = data[2]
        if request.POST:
                new_data = request.POST.copy()
                data = new_data['data'].split('|')[2]
                exist = Tematy.objects.filter(klasa=new_data['klasa'],godzina=new_data['godzina'],data=data)
                if new_data['tresc'].strip()!='':
                        if exist: id=exist[0].id
                        new_temat = Tematy(id=id,klasa_id=new_data['klasa'],godzina_id=new_data['godzina'],
                                   data=data,tresc=new_data['tresc'])
                        new_temat.save()
                if exist and new_data['tresc'].strip()=='':exist[0].delete()
        cache.set('klasa',klasa_id,86400)
        now = datetime.date.today()
        dzien= '%s-%s-%s' % (now.year,now.month,now.day)
        return render_to_response('tematy.html',{'dzien':dzien,'header':'Tematy zajęć','tydzien':pobierz_tydzien(year,month,day),
                                                 'data':date},
                                               context_instance=RequestContext(request))

def check_login(request,login):
        #u = User.objects.create_user(username='jaro',password='szakal',email='lennon@thebeatles.com')
        #u.save()
        user = User.objects.filter(username=login)
        if user:return HttpResponse('exist')
        #if user:return HttpResponse("<font face=arial size=1 color='blue'>Podany login już istnieje,proszę wybrać inny.</font>")
        #return HttpResponse("<font face=arial size=1 color='green'>Login jest dostępny.</font>")
        return HttpResponse('ok')
