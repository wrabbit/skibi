# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group,Message
from e_dziennik.models import *
from stats.models import UserActivity
from django.core.cache import cache
import datetime

def wczytaj_menu(request,klasa_id):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        try:
                klasa = Klasy.objects.get(id = klasa_id)
                request.session['klasa_id']=klasa_id
                request.session['klasa']=klasa
        finally:
                return HttpResponseRedirect('/loged/?page=1')
                #return render_to_response('base_tresc.html',context_instance=RequestContext(request))

def pobierz_dane(request,dziecko=None,page=None):
        
        if request.GET.has_key('page'):
                return object_list(request,
                           queryset=Aktualnosci.objects.all().order_by('-news_date'),
                           paginate_by = 2,
                           page = page,
                           extra_context={'header':'Aktualności'},
                           template_name = 'base_tresc.html')
        if request.POST:
                
                username = request.POST['username']
                password = request.POST['passwd']
                user = authenticate(username=username, password=password)
                
        if user is not None and user.is_active:
                last_login = user.last_login
                login(request, user) # zapisuje ID uzytkownika w sesji(inaczej request.user=AnonymousUser)
                
                klasy_w = Klasy.objects.filter(wychowawca=request.user.id)
                klasy_n = Przedmioty.objects.filter(nauczyciel=request.user.id).values('klasa').distinct()
                przedmioty_n = Przedmioty.objects.filter(nauczyciel=request.user.id)
                if user.groups.count()==1 and user.groups.filter(name='Administrator'):
                        return HttpResponseRedirect('/admin')
                if klasy_w:klasa_id = klasy_w[0].id
                elif klasy_n: klasa_id = klasy_n[0]['klasa']
                
                else:
                        dziecko = Uczniowie_tmp.objects.get(uczenprofile__rodzic = request.user.id)
                        klasa_id = dziecko.klasa.id
                klasa = Klasy.objects.get(id = klasa_id)
                tmp = Przedmioty()
                news = Aktualnosci.objects.all()
                klasy_n = tmp.klasy_nauczycieli(klasy_n)
                request.session['last_login']=last_login
                request.session['klasa']=klasa
                request.session['klasa_id']=klasa_id
                request.session['klasy_w']=klasy_w
                request.session['klasy_n']=klasy_n
                request.session['przedmioty_n']=przedmioty_n
                request.session['dziecko'] = dziecko
                grupa = Group.objects.filter(user__id=request.user.id)
                grupa = [g.name for g in grupa]
                #return render_to_response('base_tresc.html',{'header':'Aktualnosci','news':news}
                #                                  ,context_instance=RequestContext(request))
   

                return object_list(request,
                           queryset=Aktualnosci.objects.all().order_by('-news_date'),
                           paginate_by = 2,
                           page = page,
                           extra_context={'header':'Aktualności','last_login':last_login},
                           template_name = 'base_tresc.html')
        else:
                return HttpResponseRedirect('/')
        		
from django.contrib.auth import logout

def wyloguj(request):
        logout(request)
        return HttpResponseRedirect('/')

from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django import oldforms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


def password_change(request,klasa_id,header,template_name='reg/pasword_change_form.html'):
    if not request.user.is_authenticated():return HttpResponseRedirect('/')
    new_data, errors = {}, {}
    form = PasswordChangeForm(request.user)
    if request.POST:
        new_data = request.POST.copy()
        errors = form.get_validation_errors(new_data)
        if not errors:
            form.save(new_data)
            return HttpResponseRedirect('/'+klasa_id+'/password_change/done/')
    return render_to_response(template_name, {'form': oldforms.FormWrapper(form, new_data, errors),
                                              'header':header},context_instance=RequestContext(request))


def password_change_done(request,klasa_id,template_name='reg/pasword_change_done.html'):
    return render_to_response(template_name,context_instance=RequestContext(request))


#newforms

from django import newforms as forms
from django.newforms import fields

class PMessage(forms.Form):

        Odbiorca = forms.ChoiceField(choices = (), widget = forms.Select)
        Temat = forms.CharField(max_length=30)
	Tresc = forms.CharField(widget=forms.Textarea)

def get_odbiorcy(klasa_id,send,all_n=('',[]),all_r=('',[])):
        """Zwraca liste odbiorcow wiadomosci i e-maili"""

        n = User.objects.filter(przedmioty__klasa=klasa_id).distinct() #nauczyciele w danej klasie
        r = User.objects.filter(uczenprofile__klasa=klasa_id).distinct()  #rodzice w danej klasie
        # e-mail
        if len(n)!=0 and send=='email':all_n = ('\n',[(','.join([i.email for i in n]),'--wszyscy nauczyciele--')])
        if len(r)!=0 and send=='email':all_r = ('\n',[(','.join([i.email for i in r]),'--wszyscy rodzice--')])
        # message
        if len(n)!=0 and send=='msg':all_n = ('\n',[([int(i.id) for i in n],'--wszyscy nauczyciele--')])
        if len(r)!=0 and send=='msg':all_r = ('\n',[([int(i.id )for i in r],'--wszyscy rodzice--')])
        odbiorcy = (('Nauczyciele',[(i.id,i.first_name+' '+i.last_name) for i in n]),all_n,
                    ('Rodzice',[(i.id,i.first_name+' '+i.last_name) for i in r]),all_r)
        return odbiorcy


from django.core.mail import send_mail
def email_send(request,header,klasa_id,target_user=None):
        """Wysylanie wiadomosci e-mail z pomoca funkcji send_mail oraz newforms"""
	if request.user.is_authenticated():
		if request.method == 'POST':
                        # formularz z danymi z POST
                        form = PMessage(request.POST)
                        form.fields['Odbiorca'] = forms.GroupedChoiceField(choices=get_odbiorcy(klasa_id,'email'))
		        if form.is_valid():
                                #dane poprawne
                                new_data = request.POST.copy()
			        target = new_data['Odbiorca']
			        #return HttpResponse(str(target))
			        try: target = int(target)
			        except: pass
				if type(target) is int :
                                        ruser = User.objects.get(id=target)
                                        target = [ruser.email]        
                                else: target = target.split(',')
				send_mail(new_data['Temat'], new_data['Tresc'],'', target, fail_silently=False)                                                                    
				return HttpResponseRedirect('/'+klasa_id+'/email_send/done/')
			else:
                                # dane niepoprawne
			        return render_to_response('msg/email_newsform.html', {'f':form,'header':header},
                                                          context_instance=RequestContext(request))
                else:
                        # formularz
                        form = PMessage()
                        form.fields['Odbiorca'] = forms.GroupedChoiceField(choices=get_odbiorcy(klasa_id,'email'))
                        return render_to_response('msg/email_newsform.html', {'f':form,'header':header},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/")

def email_send_done(request,klasa_id,template_name='msg/email_send_done.html'):
    return render_to_response(template_name, {'path':request.path[:-5],
                                              'klasa':klasa_id},context_instance=RequestContext(request))

from django.views.generic.list_detail import object_list

def sprawdz_msg(request,header,page=None):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        """Sprawdz wiadomosci od uzytkownikow"""
        return object_list(request,
                           queryset=Wiadomosci.objects.filter(user=request.user.id).order_by('-dodano'),
                           paginate_by = 2,
                           page = page,
                           extra_context={'header':header},
                           template_name = 'msg/check_message.html')

from django.newforms import form_for_model



	
def message_send(request,klasa_id,header,error=False):
        """Wysylanie wiadomosci za pomoca modelu Message oraz newforms(form_for_model)"""
        if request.user.is_authenticated() :
                if request.user.has_perm('e_dziennik.add_wiadomosci'):
                        MessageForm = form_for_model(Wiadomosci)
                        form = MessageForm()
                        form.fields['user'] = forms.GroupedChoiceField(choices=get_odbiorcy(klasa_id,'msg'))
                        if request.method == 'POST':
                                new_data = request.POST.copy()
                                new_data['user']= new_data['user'].strip('[]').split(',')[0]
                                new_data['sender']=request.user.get_full_name()
                                form = MessageForm(new_data)
                                if form.is_valid():
                                        if new_data.has_key('sms'):
                                                #wyslanie sms-a
                                                import sms_orangembox
                                                from sms_orangembox import *
                                                phones=[]
                                                for e in request.POST['user'].strip('[]').split(','):
                                                        u = User.objects.get(id = e)
                                                        if u.mobile_phone != None:phones.append(u.mobile_phone)
                                                if len(phones)==0:error=True
                                                else:
                                                        for n in phones:sendsms(new_data['sender'],str(n),new_data['message'])
                                        else:
                                                #wyslanie wiadomosci
                                                new_msg=form.save(commit=False)
                                                new_msg.multi_msg(request.POST['user'].strip('[]').split(','))
                                        return render_to_response('msg/message_send_done.html',{'path':request.path,'error':error},
                                                                  context_instance=RequestContext(request))
                                else:
                                        form.fields['user'] = forms.GroupedChoiceField(choices=get_odbiorcy(klasa_id,'msg'))
                                        return render_to_response('msg/message_send_form.html',
                                                                  {'f':form},context_instance=RequestContext(request))
                        else:
                                return render_to_response('msg/message_send_form.html',{'f':form,'header':header},
                                                          context_instance=RequestContext(request))
                else:
                        #raise Http404
                        return HttpResponseRedirect('/perm/wiadomosci/')            
        else: return HttpResponseRedirect("/")

def message_send_done(request,klasa_id,template_name='msg/message_send_done.html'):
    return render_to_response(template_name, {'path':request.path[:-5]},context_instance=RequestContext(request))
        
def usun_msg(request,klasa_id,msg_id):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        rekord = Wiadomosci.objects.filter(id = msg_id)
        rekord.delete()
        return HttpResponseRedirect('/sprawdz_msg/')

        
def historia_zdarzen(request,user_id,header,page=None):
        if not request.user.is_authenticated():return HttpResponseRedirect('/')
        return object_list(request,
                           queryset=UserActivity.objects.filter(user = user_id).order_by('-date'),
                           paginate_by = 20,
                           page = page,
                           extra_context={'header':header},
                           template_name = 'historia.html')
