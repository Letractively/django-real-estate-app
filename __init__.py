from django.core.exceptions import ImproperlyConfigured

try:
	import sorl
except ImportError:
	raise ImproperlyConfigured("You need install sorl-thumbnail app")

try:
	import captcha
except ImportError:
	raise ImproperlyConfigured("You need install django-simple-captcha app")

def get_apps():
	return [
		'real_estate_app',
		'real_estate_app.apps.real_estate_files',
		'real_estate_app.apps.realtors',
		'real_estate_app.apps.newspapers',
		'real_estate_app.apps.portlets',
		'real_estate_app.apps.propertys',
		'real_estate_app.apps.photos',
		'real_estate_app.apps.marketing',
		'real_estate_app.apps.visitcalendar'
	]