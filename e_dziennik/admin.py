from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response

from django.contrib.auth.models import User,Group






def view_n(request):
	y = Group.objects.filter(name='Nauczyciel')
	for i in y :
	    nauczyciel = User.objects.filter(groups = i.id)
	return render_to_response('index_tresc.html',{'nauczyciel':nauczyciel})


from django import forms

def dodaj_nauczyciel(request):
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
            return HttpResponseRedirect("Lista nauczycieli/")
    else:
        # Brak danych POST, chcemy czysty formularz
        errors = new_data = {}

    # Tworzymy wrappera, szablon i reszte
    form = forms.FormWrapper(manipulator,new_data,errors)
    return render_to_response('forms_admin.html', {'form': form,'tytul': 'Dodaj nauczyciela'})
    





	

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
    return render_to_response('forms_admin.html', {'form': form, 'osoba': osoba,'tytul': 'Edycja nauczycieli'})