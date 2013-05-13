from django.conf.urls.defaults import url

contact = url(
	regex  = '^contact/$',
	view   = 'real_estate_app.views.contact',
	name   = 'contact'
)
