# Django settings for e_szkola project.

<<<<<<< HEAD:settings.py
=======

>>>>>>> 32f34afc775f6ccadc86268aa53a6f7045414a07:settings.py
DEBUG = True
TEMPLATE_DEBUG = DEBUG
#APPEND_SLASH=False
#AUTH_PROFILE_MODULE = 'e_dziennik.UserProfile'
ADMINS = (
    (('Marcin', 'm.straszynski@gmail.com'), ('Kleiner', 'kleiner1@op.pl'))
)
SERVER_EMAIL = 'm.straszynski@gmail.com'
#E-MAIL

#gmail.com
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'marcins.contact@gmail.com'
EMAIL_HOST_PASSWORD = 'marcinss'
EMAIL_PORT = 587

#poczta.onet.pl
#EMAIL_HOST = 'smtp.poczta.onet.pl'
#EMAIL_HOST_USER = 'kleiner1@op.pl'
#EMAIL_HOST_PASSWORD = 'gajger45'


MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
<<<<<<< HEAD:settings.py
DATABASE_NAME = 'my_245'             # Or path to database file if using sqlite3.
DATABASE_USER = 'my_245a'             # Not used with sqlite3.
DATABASE_PASSWORD = 'gajger45'         # Not used with sqlite3.
DATABASE_HOST = 'sql.w-rabbit.megiteam.pl'             # Set to empty string for localhost. Not used with sqlite3.
=======
DATABASE_NAME = 'e-dziennik'             # Or path to database file if using sqlite3.
DATABASE_USER = 'marcin'             # Not used with sqlite3.
DATABASE_PASSWORD = 'gajger'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
>>>>>>> 32f34afc775f6ccadc86268aa53a6f7045414a07:settings.py
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Warsaw'
#DATABASE_OPTIONS = {'use_unicode': True, 'charset': 'utf8'}
#DATABASE_OPTIONS = {'use_unicode': False, 'charset': 'utf8'}
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pl'

SITE_ID = 1
VALID_TAGS = ('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote')

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
<<<<<<< HEAD:settings.py
MEDIA_ROOT = 'site_media/'
=======
MEDIA_ROOT = 'C:/xampp/htdocs/wisz_dziennik/e_szkola/site_media/'
>>>>>>> 32f34afc775f6ccadc86268aa53a6f7045414a07:settings.py

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$me=6n)3z(wbaowu&v^^r51o8(64g0@zfp2-^mvc+36p!%c7f^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
     'django.template.loaders.eggs.load_template_source',
)
#CACHOWA NIE:
#memcache
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
#dbcache
#CACHE_BACKEND = 'db://cache_table'
#filesystemcache
#CACHE_BACKEND = 'file://c:/tmp/django_cache'


#CACHE_MIDDLEWARE_SECONDS = 60 * 60 # 60 minutes
#CACHE_MIDDLEWARE_KEY_PREFIX = 'e-dziennik'
#CACHE_MIDDLEWARE_GZIP = True
#CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
LOGIN_REDIRECT_URL='/'
LOGIN_URL='/'
LOGOUT_URL ='/'
<<<<<<< HEAD:settings.py
AUTO_LOGOUT_DELAY = 10  #10 minut

MIDDLEWARE_CLASSES = (
    
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
=======
AUTO_LOGOUT_DELAY = 20  #10 minut

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware' ,
>>>>>>> 32f34afc775f6ccadc86268aa53a6f7045414a07:settings.py
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
	
	#'django.middleware.cache.CacheMiddleware',
<<<<<<< HEAD:settings.py
	'e_szkola.stats.middleware.statsMiddleware',
	'e_szkola.stats.middleware.StatsSiteMiddleware',
	'e_szkola.stats.middleware.AutoLogout',
	'e_szkola.stats.middleware.Activity',
=======
	'stats.middleware.statsMiddleware',
	'stats.middleware.StatsSiteMiddleware',
	'stats.middleware.AutoLogout',
	#'stats.middleware.Activity',
>>>>>>> 32f34afc775f6ccadc86268aa53a6f7045414a07:settings.py
	
)
#sesja
#SESSION_ENGINE="django.contrib.sessions.backends.file" # sesja do pliku
#SESSION_FILE_PATH
#SESSION_ENGINE="django.contrib.sessions.backends.cache" # sesja do cache
<<<<<<< HEAD:settings.py
#SESSION_COOKIE_AGE = 15
=======
#SESSION_COOKIE_AGE = 1200
>>>>>>> 32f34afc775f6ccadc86268aa53a6f7045414a07:settings.py
#SESSION_COOKIE_DOMAIN
#SESSION_COOKIE_NAME 
#SESSION_COOKIE_SECURE
SESSION_EXPIRE_AT_BROWSER_CLOSE=True

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
<<<<<<< HEAD:settings.py
	'templates',
)
'''
AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'e_szkola.sslauth.backends.SSLAuthBackend',
)
'''
INTERNAL_IPS = [
 
] 

=======
	'C:/xampp/htdocs/wisz_dziennik/e_szkola/templates',
)

INTERNAL_IPS = [
] 

SITE_KEY = 'localhost:8080'

>>>>>>> 32f34afc775f6ccadc86268aa53a6f7045414a07:settings.py
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
<<<<<<< HEAD:settings.py
	"e_szkola.e_dziennik.context_processors.variables",
=======
	"e_dziennik.context_processors.variables", #plik context_processors.py z funkcja variables dodajaca zmienne do wszystkich szablonow
>>>>>>> 32f34afc775f6ccadc86268aa53a6f7045414a07:settings.py
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
<<<<<<< HEAD:settings.py
    #'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.sitemaps',
        'e_szkola.cal',
	'e_szkola.userpanel',
	'e_szkola.boxcomments',
	'e_szkola.myghtyboard',
	'e_szkola.e_dziennik',
	'e_szkola.ustawienia',
	'e_szkola.stats',

)
=======
    'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.sitemaps',
	
	'userpanel',
	'boxcomments',
	'myghtyboard',
	'cal',
	'e_dziennik',
	'ustawienia',
	'stats',

)
>>>>>>> 32f34afc775f6ccadc86268aa53a6f7045414a07:settings.py
