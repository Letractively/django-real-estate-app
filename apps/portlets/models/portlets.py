# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from real_estate_app.models import RealEstateAppCompleteModel
from real_estate_app.apps.newspapers.models import News

TYPES=(
	('newspapers.News',_('News')),
	('marketing.MarketingObject',_('Marketing Object')),
	('real_estate_files.Files',_('File')),
	('propertys.Property',_('Property')),
)

class Portlet(RealEstateAppCompleteModel):
	
	featured=models.IntegerField(
							_('Featured object'),
							help_text=_('Entry with a featured news'),
							blank=True,
							null=True
	)

	amount_featured = models.IntegerField(
							_('Amount of featured news'),
							help_text=_('Amount of featured news to display'),
	)

	type_portlet = models.CharField(
							_('Type of portlet'),
							max_length=255,
							choices=TYPES,
							blank=False,
							default='news'
	)

	def _get_type_portlets(self):
		if self.type_portlet:
			return dict(TYPES)[self.type_portlet]
		return None
	typeportlet=property(_get_type_portlets)


	def __unicode__(self):
		return u'%s' % self.title

	class Meta:
		app_label            = 'portlets'
		db_table             = 'real_estate_app_apps_portlets_portlet'
		verbose_name         = _('Portlet')
		verbose_name_plural  = _('Portlets')
		unique_together      = ('title','type_portlet')
