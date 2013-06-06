# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from real_estate_app.models import RealEstateAppBaseModel
from real_estate_app.managers import RealEstateManager

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

class VisitEvent(RealEstateAppBaseModel):

	property_fk = models.ForeignKey('propertys.Property')

	visitor_fk = models.ForeignKey('visitcalendar.Visitor')

	date_visit = models.DateTimeField(
							_('Date of visit'),
							unique=True,
							default=datetime.now(),
							help_text=_('Entry with a init of date publicashion')
	)

	slug = models.SlugField(
        _('slug'),
        unique=True,
        help_text=_('Automatically built from the caption. A slug is a short '
                    'label generally used in URLs.'),
    )

	objects = RealEstateManager()

	class Meta:
		app_label = 'visitcalendar'
		db_table  = 'real_estate_app_apps_visitcalendar_visitevent'
		get_latest_by='date_visit'
		ordering=('date_visit',)
		verbose_name=_('Visit')
		verbose_name_plural=_('Visits')

	def __unicode__(self):
		try:
			return '%s' % self.date_visit.strftime(settings.DATETIME_INPUT_FORMATS[0])
		except IndexError:
			return '%s' % self.date_visit.strftime('%Y-%m-%d %H:%M:%S')
		else:
			raise

	def _visitor(self):
		return self.visitor_first_name+' '+self.visitor_last_name
	visitor=property(_visitor)

	def _get_absolute_url(self):
		return ('visitcalendar-detail',None, {
				'slug' : str(self.slug),
				})
	get_absolute_url=permalink(_get_absolute_url)