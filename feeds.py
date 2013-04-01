# -*- coding: utf-8; -*-
from django.contrib.syndication.views import Feed
from models import Property, News
from conf.settings import REAL_ESTATE_APP_SITE_NAME, REAL_ESTATE_APP_NUM_LATEST

class PropertyFeed(Feed):
	title=REAL_ESTATE_APP_SITE_NAME 
	link="/imoveis/"
	description="The lastested property uploaded."


	def items(self):
		return Property.objects.all()

	def item_title(self,item):
		return u'[%s] %s'%(item.statusproperty_fk,item.address)

	def item_description(self, item):
		return item.description

class NewsFeed(Feed):
	title=REAL_ESTATE_APP_SITE_NAME 
	link="/imoveis/news/"
	description="The lastested news uploaded."


	def items(self):
		return News.objects.all()

	def item_title(self,item):
		return u'%s' % item.title

	def item_description(self, item):
		return item.content