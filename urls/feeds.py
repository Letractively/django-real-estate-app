from django.conf.urls.defaults import url
from real_estate_app.feeds import PropertyFeed

feeds_url = url(
	regex  ='^rss/$',
	view   = PropertyFeed(),
	name   = 'property-feeds'
)
