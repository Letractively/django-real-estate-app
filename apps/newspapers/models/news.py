# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from real_estate_app.models import RealEstateAppCompleteModel

class News(RealEstateAppCompleteModel):

	content = models.TextField(
					_('Content'),
					null=True,
					blank=True
	)

	def __unicode__(self):
		return u'%s' % (self.title)

	class Meta:
		app_label           = 'newspapers'
		db_table            = 'real_estate_app_apps_newspapers_news'		
		get_latest_by       = 'pub_date'
		ordering            = ('-pub_date',)
		verbose_name        = _('News')
		verbose_name_plural = _('News')

	@permalink
	def get_absolute_url(self):
		return ('newspapers-detail', None, {
				'slug' : str(self.slug),
				})
