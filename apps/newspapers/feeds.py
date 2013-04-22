# -*- coding: utf-8; -*-
from django.contrib.syndication.views import Feed
from models import News
from real_estate_app.conf.settings import REAL_ESTATE_APP_SITE_NAME, REAL_ESTATE_APP_NUM_LATEST

class NewsFeed(Feed):
	title=REAL_ESTATE_APP_SITE_NAME
	# TODO: Better the link
	link="/imoveis/news/"
	description="The lastested news uploaded."


	def items(self):
		return News.objects.all()

	def item_title(self,item):
		return u'%s' % item.title

	def item_description(self, item):
		return item.content