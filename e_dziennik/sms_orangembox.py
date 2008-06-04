import cookielib, string, urllib, urllib2
from ustawienia.models import Ustawienia




konta = Ustawienia.objects.filter(opis='sms')
konto1 = konta[0]

debug = 0   # for debug change to '1'
freesms = 0     # for smses left change to '1'
phonebook = 'phonebook.txt'
login = konto1.login  # set login
password = konto1.haslo # set password

def _phonebook(name):
        try:
                plik = open (phonebook, 'r')
        except IOError:
                print 'Error. File "%s" not found.' % phonebook
                sys.exit(1)
        else:
                for line in plik.readlines():
                        if name in line:
                                name = line.split()[-1]
                                return name
                                try:
                                        plik.close()
                                except IOError:
                                        print 'Error. File "%s" not found.' % phonebook
                                        sys.exit(1)

def sendsms(sender, recipient, message):
        if recipient.isalpha():
                number = _phonebook(recipient)
                if number is None:
                        print 'Error. Recipient "%s" not found.' % recipient
                        sys.exit(1)
        if recipient.isdigit():
                number = recipient
        if len(sender) > 0 and number.isdigit() and len(number) == 9 and len(message) > 0:
                baseURL='http://www.orange.pl'
                length = 634 - len(message) - len(sender)
                cj = cookielib.CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# orange signin
                request = urllib2.Request(baseURL + '/portal/map/map/signin')
                request.add_header('User-Agent', 'Opera/8.00 (Windows NT 5.0; U; en)')
                try:
                        result = opener.open(request)
                        if debug:
                                print 'Connecting with',baseURL
                except IOError:
                        print 'Connection with %s failed.' % baseURL
# orange login
                parmdicta = {'_dyncharset' : 'UTF-8',
                '/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.loginErrorURL': 'http://www.orange.pl/portal/map/map/signin',
                '_D:/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.loginErrorURL': ' ',
                '/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.loginSuccessURL': 'http://www.orange.pl/portal/map/map/pim',
                '_D:/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.loginSuccessURL': ' ',
                '/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.value.login' : login,
                '_D:/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.value.login' : ' ',
                '/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.value.password' : password,
                '_D:/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.value.password' : ' ',
                '/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.login.x' : '0',
                '/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.login.y' : '0',
                '_D:/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.login' : ' ',
                '_DARGS': '/gear/static/signInLoginBox.jsp'}
                request = urllib2.Request(baseURL + '/portal/map/map/signin?_DARGS=/gear/static/signInLoginBox.jsp')
                postdata = urllib.unquote(urllib.urlencode(parmdicta))
                request.add_data(postdata)
                request.add_header('User-Agent', 'Opera/8.00 (Windows NT 5.0; U; en)')
                try:
                        result = opener.open(request)
                        if debug:
                                print 'Logged.'
                except IOError:
                        print 'Not logged.'
# orange SMS form
                request = urllib2.Request(baseURL + '/portal/map/map/message_box?mbox_view=newsms&mbox_edit=new')
                request.add_header('User-Agent', 'Opera/8.00 (Windows NT 5.0; U; en)')
                try:
                        result = opener.open(request)
                        if debug:
                                print 'Opening SMS form.'
                except IOError:
                        print 'Open SMS form failed.'
# Send SMS
                parmdictb = {'_dyncharset' : 'UTF-8',
                '/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.type': 'sms',
                '_D:/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.type' : ' ',
                'enabled' : 'false',
                '/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.errorURL' : '/portal/map/map/message_box?mbox_view=newsms',
                '_D:/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.errorURL' : ' ',
                '/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.successURL' : '/portal/map/map/message_box?mbox_view=messageslist',
                '_D:/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.successURL' : ' ',
                'smscounter' : '1',
                'counter' : length,
                '/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.to' : number,
                '_D:/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.to' : ' ',
                '_D:/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.body' : ' ',
                '/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.body' : 'Od '+sender+' : '+message,
                '/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.create.x' : '0',
                '/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.create.y' : '0',
                '/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.create' : 'Wyslij',
                '_D:/amg/ptk/map/messagebox/formhandlers/MessageFormHandler.create' : ' ',
                '_DARGS' : '/gear/mapmessagebox/smsform.jsp'}
                request = urllib2.Request(baseURL + '/portal/map/map/message_box?_DARGS=/gear/mapmessagebox/smsform.jsp')
                postdata = urllib.unquote(urllib.urlencode(parmdictb))
                request.add_data(postdata)
                request.add_header('User-Agent', 'Opera/8.00 (Windows NT 5.0; U; en)')
                try:
                        result = opener.open(request).read()
                        if freesms:
                                import re
                                rw = re.compile(r'<span class="value">(\d+)',re.S)
                                for sms in rw.findall(result):
                                        print sms
                        if debug:
                                print 'SMS sent.'
                except IOError:
                        print 'SMS not sent.'
# Logout
                parmdictc = {'_dyncharset' : 'UTF-8',
                '/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.logoutSuccessURL' : '/portal/map/map',
                '_D:/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.logoutSuccessURL' : ' ',
                '/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.logoutErrorURL' : '/portal/map/map',
                '_D:/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.logoutErrorURL' : ' ',
                'enabled' : 'true',
                '/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.logout.x' : '0',
                '/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.logout.y' : '0',
                '/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.logout' : 'logout',
                '_D:/amg/ptk/map/core/formhandlers/AdvancedProfileFormHandler.logout' : ' ',
                '_DARGS' : '/portal/layoutTemplates/html/user_status.jsp'}
                request = urllib2.Request(baseURL + '/portal/map/map?_DARGS=/portal/layoutTemplates/html/user_status.jsp')
                postdata = urllib.unquote(urllib.urlencode(parmdictc))
                request.add_data(postdata)
                request.add_header('User-Agent', 'Opera/8.00 (Windows NT 5.0; U; en)')
                try:
                        result = opener.open(request)
                        if debug:
                                print 'Logout.'
                except IOError:
                        print 'Logout error.'
# Main
if __name__ == '__main__':
        import sys
        if len(sys.argv) < 4:
                print 'Sposob uzycia:', sys.argv[0], '<nadawca> <nazwa lub numer odbiorcy> <wiadomosc>'
                print 'Przyklad 1:', sys.argv[0], 'inspektor 501234567 bardzo byc moze ale zaba pozostaje zaba'
                print 'Przyklad 2:', sys.argv[0], 'sprzedawca pralinka najprawdopodobniej usycha z teskonty za fiordami'
                sys.exit(1)
        sender, recipient, message = sys.argv[1], sys.argv[2], ' '.join(sys.argv[3:])
        sendsms(sender, recipient, message) 
