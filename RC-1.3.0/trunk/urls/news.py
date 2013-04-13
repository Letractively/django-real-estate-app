from django.conf.urls.defaults import url
from real_estate_app.conf.settings import REAL_ESTATE_APP_NUM_LATEST
from real_estate_app.feeds import NewsFeed 

info_dict = {
    'template_object_name': 'news',
}

feeds_news = {
 	'rss': NewsFeed,
}

news_list = url(
    regex  = '^news/$',
    view   = 'real_estate_app.views.news.news_list',
    kwargs = dict(info_dict, paginate_by=REAL_ESTATE_APP_NUM_LATEST),
    name   = 'news-list'
)


news_detail = url(
	regex  = '^news/(?P<slug>[-\w]+)/$',
	view   = 'real_estate_app.views.news.news_detail',
	kwargs = dict(info_dict, slug_field='slug'),
	name   = 'news-detail'
)