# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _


class News(models.Model):

	title = models.CharField(
					_('Title'),
					max_length=255,
					blank=True,
					null=True
	)
	
	slug= models.SlugField(
					_('Slug'),
					unique=True
	)

	content = models.TextField(
					_('Content'),
					null=True,
					blank=True
	)
	
	link = models.CharField(
					_('Link'),
					null=True,
					blank=True,
					max_length=600,
	)

	pub_date = models.DateField(
				default=datetime.now()
	)

	enable_publish = models.BooleanField(
							_('Enable publish'), 
							default=True
	)

	def __unicode__(self):
		return u'%s' % (self.title)

	class Meta:
		app_label='real_estate_app'		
		get_latest_by='pub_date'
		ordering=('-pub_date',)
		verbose_name=_('News')
		verbose_name_plural=_('News')

	@permalink
	def get_absolute_url(self):
		return ('news-detail', None, {
				'slug' : str(self.slug),
				})
