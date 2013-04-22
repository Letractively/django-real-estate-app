from django.conf.urls.defaults import url
from django.contrib.sitemaps import GenericSitemap

from real_estate_app.conf.settings import REAL_ESTATE_APP_NUM_LATEST

from feeds import NewsFeed 
from models import News 

info_dict = {
    'template_object_name': 'news',
}

feeds_news = {
 	'rss': NewsFeed,
}

newspapers_info = {'queryset':News.objects.all(),}
sitemap_info = {'proprety':GenericSitemap(newspapers_info,priority=0.8),}

newspapers_list = url(
    regex  = '^news/$',
    view   = 'real_estate_app.apps.newspapers.views.news_list',
    kwargs = dict(info_dict, paginate_by=REAL_ESTATE_APP_NUM_LATEST),
    name   = 'newspapers-list'
)

newspapers_detail = url(
	regex  = '^news/(?P<slug>[-\w]+)/$',
	view   = 'real_estate_app.apps.newspapers.views.news_detail',
	kwargs = dict(info_dict, slug_field='slug'),
	name   = 'newspapers-detail'
)

feeds_newspapers_url = url(
	regex  = '^news/rss/$',
	view   = NewsFeed(),
	name   = 'proprety-feeds'
)

newspapers_sitemap = url(
	regex  = '^news/sitemap\.xml$', 
	view   = 'django.contrib.sitemaps.views.sitemap', 
	kwargs = dict(sitemaps=sitemap_info),
	name   = 'newspapers-sitemap'
)