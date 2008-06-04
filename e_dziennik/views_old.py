# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group

def sprawdz_login(request):

	if request.POST:
		username = request.POST['username']
		password = request.POST['passwd']
        user = authenticate(username=username, password=password)
        if user is not None:
			login(request, user)	
           			
			# pobierz imie i nazwisko na podstawie loginu
			dane = User.objects.filter(username=username) # for
			#u = User.objects.get(username__exact=username)  => dane=u.get_full_name()
			#all_users =User.objects.all()   => dane = all_users.filter/exclude(username=username)
			
			
			#pobierz czlonkowstwo uzytkownika w grupie na podstawie loginu
			grupa = Group.objects.filter(user__username=username) 
		    #all_gropus =Group.objects.all()  => grupa=all_groups.filter(user__username=username)
			menu =['Oceny','Nieobecnosci','Uwagi','Plan lekcji','Lista uczniow','Lista przedmiotow','Raporty','Ustawienia','Dni pracy','Godziny lekcyjne','Sale lekcyjne','Lista przedmiotow','Wagi ocen','Wartosci ocen','Lista nauczycieli']
			for g in grupa:
			    if g.name == 'Wychowawcy' or g.name == 'Nauczyciele':
			        menu = menu[:8]
			    elif g.name =='Administratorzy':
				    menu = menu[-7:]
			    elif g.name =='Rodzice':
				    menu = menu[:4]
			
			return render_to_response('index_tresc.html',{'dane' : dane,'grupa' : grupa,'menu':menu})
			
		    	
        else:
	        #return render_to_response('login_tresc.html',{'info':'Bledny login lub haslo'})
			#return HttpResponseRedirect('/?next=%s' % request.path)
			return HttpResponseRedirect('/')
		

		
from django.contrib.auth import logout

def wyloguj(request):
    logout(request)
    return HttpResponseRedirect('/')

	
from django import forms

def lista_nauczycieli(request):
    manipulator = User.AddManipulator()

    if request.POST:
        # dane wyslane POSTem, kopiujemy je i chcemy tworzyc nowy obiekt Place
        new_data = request.POST.copy()

        # Sprawdzamy bledy
        # jezeli beda formularz przeladuje sie zachowujac dane
        # bo sa one w new_data
        errors = manipulator.get_validation_errors(new_data)

        if not errors:
            # Brak bledow czyli zapisujemy!
            manipulator.do_html2python(new_data)
            new_place = manipulator.save(new_data)

           # przekierowanie na widok wpisow
           # zawsze po wyslaniu formularza gdzies
           # przekierowuj by uniknac dodawania klonow danych
            return HttpResponseRedirect("/view/")
    else:
        # Brak danych POST, chcemy czysty formularz
        errors = new_data = {}

    # Tworzymy wrappera, szablon i reszte
    form = forms.FormWrapper(manipulator,new_data,errors)
    return render_to_response('forms.html', {'form': form,'tytul': 'Dodaj nauczyciela'})
    


def view(request):
	y = Group.objects.filter(name='Nauczyciele')
	for i in y :
	    nauczyciel = User.objects.filter(groups = i.id)
	return render_to_response('index_tresc.html',{'nauczyciel':nauczyciel})


	

def edit_nauczyciel(request, user_id):
   # jezeli rekord o podanym id istnieje to stworz ChangeManipulator
    try:
        manipulator = User.ChangeManipulator(user_id)
    except User.DoesNotExist:
        raise Http404

    # Pobieramy oryginalne dane
    osoba = manipulator.original_object

    if request.POST:
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            manipulator.save(new_data)

            # przekierowanie
            return HttpResponseRedirect("/Lista nauczycieli/")
    else:
        errors = {}
        # Dzieki temu formularz poprawnie rozpozna dane dla kazdego pola
        new_data = osoba.__dict__

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('forms.html', {'form': form, 'osoba': osoba,'tytul': 'Edycja nauczycieli'})

	
	



#def wykonaj(request,opcja):
   
#   if not request.user.is_authenticated():
#       return HttpResponseRedirect('/')
#   else:
#       import string
#       return HttpResponse(string.strip(opcja,'/'))




