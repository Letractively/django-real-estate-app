# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from real_estate_app.models import RealEstateAppBaseModel
from real_estate_app.utils import alertemail
from real_estate_app.conf.settings import MANAGERS

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')
MANAGERS_EMAIL=[mail_tuple[1] for mail_tuple in MANAGERS]

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

	class Meta:
		app_label = 'visitcalendar'
		db_table  = 'real_estate_app_apps_visitcalendar_visitevent'
		get_latest_by='date_visit'
		ordering=('date_visit',)
		verbose_name=_('Visit property')
		verbose_name_plural=_('Visitors')

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
	
	msg_new=_('A new visit event has been add. \nUser: %s \nDate: %s \nLink %s') % (visitor_fk, date_visit ,get_absolute_url)

	@alertemail(_('New visit event'),msg_new,'marcello@gmail.com',['root@localhost'])
	def save(self,commit=True):
		super(VisitEvent,self).save(commit)