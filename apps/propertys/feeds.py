# -*- coding: utf-8; -*-
from django import get_version
from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed

from real_estate_app.conf.settings import REAL_ESTATE_APP_SITE_NAME, REAL_ESTATE_APP_NUM_LATEST

from models import Property


class PropertyFeed(Feed):
	title=REAL_ESTATE_APP_SITE_NAME 
	description="The lastested property uploaded."
	if get_version() <= '1.3.1':
		def link(self):
			"""
			This is needed for django 1.3.1 because of this tickect 11712.
			"""
			return reverse('newspapers-list')
	else:
		from django.core.urlresolvers import reserver_lazy
		link=reserver_lazy('newspapers-list')

	def items(self):
		return Property.objects.all()

	def item_title(self,item):
		return u'[%s] %s'%(item.statusproperty_fk,item.address)

	def item_description(self, item):
		return item.description