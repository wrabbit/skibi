from django.db import models
from ustawienia.models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _ 
class Demo(models.Model):
   
    login = models.CharField(max_length=255, verbose_name='Login')
    haslo = models.CharField(max_length=255, verbose_name='Haslo')
	
    class Meta:         
        verbose_name = "Demo"
        verbose_name_plural = "Demo"
        
    class Admin:
        list_display = ('login', 'haslo')
        list_filter = ['login']
        search_fields = ['login', 'haslo']


class Klasy(models.Model):
   
    opis = models.CharField(max_length=255, verbose_name=_('Opis'),blank=True)
    numer= models.CharField(max_length=255, verbose_name=_('Numer klasy'),help_text=_("np. 2 lub II"))
    litera = models.CharField(max_length=255, verbose_name=_('Litera'))
    wychowawca = models.ForeignKey(User)

    class Meta:
        verbose_name = "Klasa"
	verbose_name_plural = "Lista klas"
	ordering = ('numer',)	
    class Admin:
        list_display = ('id','numer', 'litera','opis','wychowawca')
        list_filter = ['numer']
        search_fields = ['numer','litera']

    def __str__(self):
        return self.numer + self.litera
 
    def _get_full_name(self):
	return  '%s %s' % (self.numer,self.litera)
    def get_uczniowie(self):
        u = Uczniowie_tmp.objects.filter(klasa = self.id)
        return u
        

    def get_przedmioty(self):
        return Przedmioty.objects.filter(klasa = self.id)


class Przedmioty(models.Model):
    obowiazkowy = models.BooleanField(blank=True,default=True)
    nazwa = models.CharField(max_length=255, verbose_name=_('Nazwa przedmiotu'))
    skrot = models.CharField(max_length=255, verbose_name=_('Nazwa skrocona'))
    klasa = models.ForeignKey(Klasy,db_index=True)
    nauczyciel = models.ForeignKey(User)
	
		
    class Meta:
        verbose_name = _("Przedmiot")
        verbose_name_plural = _("Lista przedmiotow")
	unique_together = (("klasa", "nazwa"),)
	order_with_respect_to = 'klasa'
		
    class Admin:
        list_display = ('nazwa','nauczyciel', 'klasa','obowiazkowy')
        list_filter = ['nazwa']
        search_fields = ['nazwa', 'nauczyciel']

    def __unicode__(self):
        return self.nazwa

    def klasy_nauczycieli(self,klasy_n):
        slownik_klas = {}
        for e in range(len(klasy_n)):
            j = Klasy.objects.get(id = klasy_n[e]['klasa'])
            slownik_klas[j.id]=j.numer +j.litera
        return slownik_klas

    
PLEC_TYPES = (
    ('Kobieta', 'Kobieta'),
    ('Mezczyzna', 'Mezczyzna'),

)		

class Uczniowie_tmp(models.Model):
    imie = models.CharField(max_length=255)
    nazwisko = models.CharField(max_length=255)
    numer = models.IntegerField()
    plec = models.CharField(max_length=10,choices=PLEC_TYPES,blank=True)
    kod = models.CharField(max_length=6,blank=True,verbose_name='Kod,poczta')
    miejscowosc = models.CharField(max_length=20,blank=True)
    ulica = models.CharField(max_length=20,blank=True)
    dom = models.CharField(max_length=10,blank=True,verbose_name='Dom/lokal')
    telefon = models.PhoneNumberField(blank=True,null=True)
    info = models.TextField(blank=True)
    aktualnosc = models.DateTimeField(auto_now=True,blank=True)
    utworzono = models.DateTimeField(auto_now_add=True,blank=True)
    photo = models.ImageField(_('zdjecie'),upload_to='files/photos',blank=True,null=True)
    klasa = models.ForeignKey(Klasy)
    grupa = models.ForeignKey(Grupy_jezykowe)
		
    class Meta:
        verbose_name = "UczenTmp"
        verbose_name_plural = "Lista uczniow_tmp"
        order_with_respect_to = 'klasa'
        unique_together = (("numer", "klasa"),)
        
    class Admin:
        list_display = ('imie','nazwisko', 'numer','klasa','telefon','aktualnosc')
        list_filter = ['klasa']
        search_fields = ['imie', 'nazwisko']
        
    def __str__(self):
        return self.imie + ' ' + self.nazwisko
    
    def get_full_name(self):
        full_name = u'%s %s' % (self.imie, self.nazwisko)
        return full_name.strip()
    
    def get_uwagi_all(self):
        uwagi = Uwagi.objects.filter(uczen = self.id).order_by('-dodano')
        return uwagi
    
    def get_uwagi_p(self):
        uwagi = Uwagi.objects.filter(uczen = self.id).filter(typ='Pozytywna')
        if uwagi: return len(uwagi)
        return '-'
    
    def get_uwagi_n(self):
        uwagi = Uwagi.objects.filter(uczen = self.id).filter(typ='Negatywna')
        if uwagi: return len(uwagi)
        return '-'
	    
class Wiadomosci(models.Model):
  
    user = models.ForeignKey(User,verbose_name=_('Wyslij do'))
    message = models.TextField(_('message'))
    sender = models.CharField(_('Nadawca'),max_length=50)
    dodano = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    class Meta:
        verbose_name = _('Wiadomosc')
        verbose_name_plural = _('Wiadomosci')

    class Admin:
        list_display = ('message','user','sender')

    def __unicode__(self):
        return self.message

    def multi_msg(self,odbiorcy):
        for i in odbiorcy:
            new = Wiadomosci(user_id = i, message=self.message,sender=self.sender)
            new.save()
        return True


class Oceny(models.Model):
    id = models.IntegerField('ID',primary_key=True)
    klasa = models.ForeignKey(Klasy,verbose_name=_('klasa'))
    przedmiot = models.ForeignKey(Przedmioty,verbose_name=_('przedmiot'))
    ocena = models.ForeignKey(Wartosci_ocen,verbose_name=_('ocena'))
    waga = models.ForeignKey(Wagi,verbose_name=_('waga'))
    uczen = models.ForeignKey(Uczniowie_tmp,verbose_name=_('Uczen'))
    pole = models.IntegerField(blank=True)
    data_dodania = models.DateTimeField(auto_now=True,blank=True)
    user = models.ForeignKey(User,verbose_name=_('dodana przez'))
    semestr = models.ForeignKey(Semestry,verbose_name=_('semestr'))
    class Meta:
        verbose_name = _('Ocena')
        verbose_name_plural = _('Oceny')

    class Admin:
        list_display = ('klasa','przedmiot','ocena','waga','uczen','id','pole','data_dodania','user')
    def __unicode__(self):
        return self.ocena


class Srednie(models.Model):
    id = models.IntegerField('ID',primary_key=True)
    srednia = models.FloatField(_('Srednia'))
    klasa = models.ForeignKey(Klasy,verbose_name=_('klasa'))
    przedmiot = models.ForeignKey(Przedmioty,verbose_name=_('przedmiot'))
    uczen = models.ForeignKey(Uczniowie_tmp,verbose_name=_('Uczen'))
    pole = models.IntegerField(blank=True)
    semestr = models.ForeignKey(Semestry,verbose_name=_('Semestr'))
    class Meta:
        verbose_name = _('Ocena')
        verbose_name_plural = _('Oceny')

    def __unicode__(self):
        return self.srednia

'''
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
'''
class UczenProfile(models.Model):
    uczen = models.OneToOneField(Uczniowie_tmp)
    rodzic = models.ForeignKey(User) 
    klasa = models.ForeignKey(Klasy)

class DaneUczniow(models.Model):
    plik = models.FileField(_('Plik .xls z danymi'),upload_to='files/lista uczniow',blank=True,null=True)
    opis = models.CharField(_('Opis pliku'),max_length='30',blank=True)
    class Meta:
        verbose_name_plural = _('Pliki z danymi')

    class Admin:
        list_display = ('plik','opis')
        
class PlanLekcji(models.Model):
    id = models.IntegerField('ID',primary_key=True)
    klasa = models.ForeignKey(Klasy)
    przedmiot = models.ForeignKey(Przedmioty,verbose_name=_('przedmiot'))
    godzina = models.ForeignKey(Godziny)
    dzien_tygodnia = models.CharField(_('Dzien tygodnia'),max_length=20)
    sala = models.ForeignKey(Sale)

    class Meta:
        verbose_name_plural = _('Plan lekcji')

    class Admin:
        list_display = ('klasa','przedmiot','godzina','dzien_tygodnia')

class Uwagi(models.Model):
    uczen = models.ForeignKey(Uczniowie_tmp,verbose_name=_('Uczen'))
    tresc = models.TextField(_('Tresc'))
    wystawil = models.ForeignKey(User)
    dodano = models.DateTimeField(auto_now_add =True,blank=True)
    typ = models.CharField(_('Typ'),max_length=30,choices=(('Pozytywna','Pozytywna'),('Negatywna','Negatywna')),radio_admin=True)
    potwierdzenie = models.BooleanField(_('Potwierdzenie'))
    monit = models.BooleanField(_('Monit'))
    class Meta:
        verbose_name = _('Uwaga')
        verbose_name_plural = _('Uwagi')

    class Admin:
        list_display = ('tresc','wystawil','dodano','uczen','potwierdzenie','typ','monit')

    def __unicode__(self):
        return self.tresc

    
    
class Nieobecnosci(models.Model):
    id = models.CharField('ID',max_length=20,primary_key=True)
    wartosc = models.CharField(max_length=20)
    uczen = models.ForeignKey(Uczniowie_tmp,verbose_name=_('Uczen'))
    wstawil = models.ForeignKey(User)
    data = models.DateField(blank=True)
    godzina = models.ForeignKey(Godziny)
    class Meta:
        verbose_name_plural = _('Nieobecnosci')

    class Admin:
        list_display = ('wartosc','uczen','wstawil','data','godzina')

    def __unicode__(self):
        return self.wartosc
    def get_przedmiot(self):
        import datetime
        p = PlanLekcji.objects.get(klasa=self.uczen.klasa,godzina=self.godzina,dzien_tygodnia=datetime.date.weekday(self.data))
        return p.przedmiot         

from django.contrib.sitemaps import ping_google

class Aktualnosci(models.Model):
    
    news_title = models.CharField(max_length=500,verbose_name=_('Tytul'))
    news_short = models.TextField(_('Skrot'))
    news_text = models.TextField(_('Tresc'))
    news_date = models.DateTimeField(auto_now_add = True, blank=True, verbose_name='Data dodania')
	
    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')

    class Admin:

        list_display = ('news_title', 'news_short','news_date')
        list_filter = ['news_date']
        search_fields = ['news_title', 'news_text']
        date_hierarchy = 'news_date'
	js = ['tiny_mce/tiny_mce.js', 'js/textareas.js']

    def __unicode__(self):
        return self.news_title

    def get_absolute_url(self):
	return '/news/' + str(self.id) + '/'

    def save(self):
        super(Aktualnosci, self).save()
        try:
            ping_google()
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass

class Tematy(models.Model):
    klasa = models.ForeignKey(Klasy)
    godzina = models.ForeignKey(Godziny)
    data = models.DateField()
    tresc = models.TextField()
    class Meta:
        verbose_name_plural = ('Tematy zajęć')

    class Admin:
        list_display = ('klasa','godzina','data')
