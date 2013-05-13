from django.conf.urls.defaults import url
from real_estate_app.feeds import PropertyFeed, NewsFeed

feeds_property_url = url(
	regex  ='^rss/$',
	view   = PropertyFeed(),
	name   = 'property-feeds'
)
feeds_news_url = url(
	regex  ='^news/rss/$',
	view   = NewsFeed(),
	name   = 'news-feeds'
)
