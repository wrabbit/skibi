def variables(request):
    from django.conf import settings
    is_admin = 'admin' in request.path
    if ((request.user.is_authenticated() and not request.user.is_staff)):
        return {
                'last_login':request.session['last_login'],
		'user':request.user,
		'klasy_w':request.session['klasy_w'],
		'klasy_n':request.session['klasy_n'],
		'dziecko':request.session['dziecko'],
		'przedmioty_n':request.session['przedmioty_n'],
		'klasa_obj':request.session['klasa'],
                'klasa':request.session['klasa_id']
		}
    return {'user':request.user}
	

