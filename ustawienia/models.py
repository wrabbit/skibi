from django.db import models
import string
from django.utils.translation import ugettext as _ 

OBSZAR= (('oceny','Oceny w dzienniku'),('sms','Bramka SMS'))

class Ustawienia(models.Model):
    opis = models.CharField(_('Obszar'),max_length=20,choices=OBSZAR)
    kolumny = models.PositiveIntegerField(_('Liczba kolumn'),blank=True,null=True)
    login = models.CharField(_('Login'),max_length=30,blank=True,null=True,help_text='Podaj login lub numer telefonu do bramki MultiBox,np. 510100100')
    haslo = models.CharField(_('Haslo'),max_length=30,blank=True,null=True,help_text='Podaj haslo do bramki MultiBox')
    class Meta:
	verbose_name = "Ustawienie"
	verbose_name_plural = "Ustawienia"
        
    class Admin:
        list_display = ('opis','kolumny','login','haslo')

    


class Semestry(models.Model):

    numer = models.CharField(_('Semestr'),max_length=5)
    poczatek = models.DateField(_('Data rozpoczecia'))
    koniec = models.DateField(_('Data zakonczenia'))

    class Meta:
	verbose_name = "Semestr"
	verbose_name_plural = "Lista semestrow"
	ordering = ('numer',)
        
    class Admin:
        list_display = ('numer','poczatek', 'koniec')
        
    def __str__(self):
        return self.numer

class Dni_wolne(models.Model):
    opis = models.CharField(_('Opis'),max_length=50) 
    poczatek = models.DateField(_('Data rozpoczecia'))
    koniec = models.DateField(_('Data zakonczenia'))
       

    class Meta:
	verbose_name_plural = "Dni wolne"
	verbose_name = "Dni wolne"
	ordering = ('poczatek',)
        
    class Admin:
        list_display = ('opis','poczatek','koniec',)



HOURS = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10'),)


class Godziny(models.Model):
    id = models.IntegerField('lp',primary_key=True,choices=HOURS,help_text='Numer godziny lekcyjnej')
    poczatek = models.TimeField(_('Poczatek zajec'),help_text="(HH:MM)")
    koniec = models.TimeField(_('Koniec zajec'),help_text="(HH:MM)")
    

    class Meta:
	verbose_name_plural = "Godziny lekcyjne"
	verbose_name = "Godzina lekcyjna"
	ordering = ('id',)
        
    class Admin:
        list_display = ('id','poczatek','koniec',)

    def __unicode__(self):
        return "%s-%s" % (self.poczatek,self.koniec)


class Sale(models.Model):
    numer = models.CharField(_('Numer sali'),max_length=10,unique=True) 
    nazwa = models.CharField(_('Nazwa'),max_length=30,blank=True)
    
    class Meta:
	verbose_name_plural = "Sale lekcyjne"
	verbose_name = "Sala lekcyjna"
	ordering = ('numer',)
        
    class Admin:
        list_display = ('numer','nazwa')
    
    def __str__(self):
        if self.nazwa:self.nazwa = '('+self.nazwa+')'
        return self.numer + ' ' + self.nazwa


class Wagi(models.Model):
    waga = models.PositiveIntegerField(_('Waga'),unique=True) 
    opis = models.CharField(_('Obszar oceniania'),max_length=50)
    kolor = models.CharField(_('Kolor'),max_length=20,blank=True)

    class Meta:
	verbose_name_plural = "Wagi ocen"
	ordering = ('waga',)
        
    class Admin:
        list_display = ('waga','opis','kolor')
        
    def __str__(self):
        return '%s' % self.waga



class Wartosci_ocen(models.Model):
    wartosc = models.FloatField(_('Wartosc do obliczen'),unique=True,help_text='(np. 4.33)')
    nazwa = models.CharField(_('Nazwa oceny'),max_length=2,unique=True,help_text='(np. 4+)')

    class Meta:
	verbose_name_plural = "Wartosci ocen"
	verbose_name  = string.lower("Wartosc oceny")
	ordering = ('wartosc',)
        
    class Admin:
        list_display = ('wartosc','nazwa')

    def __unicode__(self):
        return '%s' % (self.nazwa)


class Grupy_jezykowe(models.Model):
    nazwa = models.CharField(_('Nazwa grupy'),max_length=20,unique=True,help_text='(Podaj nazwę języka. Np. niemiecki,angielski,hiszpański)')

    class Meta:
	verbose_name_plural = "Grupy językowe"
	verbose_name  = string.lower("Grupa językowa")
        
    class Admin:
        list_display = ('id','nazwa')

    def __unicode__(self):
        return '%s' % (self.nazwa)
