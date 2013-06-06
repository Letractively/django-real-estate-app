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

class Visitor(RealEstateAppBaseModel):
	
	first_name = models.CharField(
		_('First name'),
		max_length=255
	)

	last_name = models.CharField(
		_('Last name'),
		max_length=255
	)

	if LANGUAGE_CODE in ('pt_BR','pt-br'):
		from django.contrib.localflavor.br.br_states import STATE_CHOICES

		cpf = models.CharField(
			u'CPF',
			max_length=11,
			unique=True,
		)

		rg = models.CharField(
			u'RG',
			max_length=20
		)

		ssp = models.CharField(
			u'SSP',
			max_length=2,
			choices=STATE_CHOICES,
			blank=True
		)

	address = models.CharField(
		_('Address'),
		max_length=255
	)

	zip = models.CharField(
		_('ZIP'),
		max_length=15
	)

	celphone = models.CharField(
		_('Celphone'),
		max_length=15
	)
	phone = models.CharField(
		_('Phone'),
		max_length=15
	)

	email = models.CharField(
		_('E-mail'),
		max_length=255
	)

	work_address = models.CharField(
		_('Work address'),
		max_length=255
	)

	work_zip = models.CharField(
		_('ZIP'),
		max_length=15
	)

	work_phone = models.CharField(
		_('Work phone'),
		max_length=15
	)

	objects=RealEstateManager()

	class Meta:
		app_label = 'visitcalendar'
		db_table  = 'real_estate_app_apps_visitcalendar_visitor'
		get_latest_by='create_date'
		ordering=('create_date',)
		verbose_name=_('Visitor')
		verbose_name_plural=_('Visitors')

	def __unicode__(self):
			return u'%s' % self.name

	def _name(self):
		return self.first_name+' '+self.last_name
	name=property(_name)

	def _get_absolute_url(self):
		return ('visitcalendar-detail',None, {
				'slug' : str(self.slug),
				})
	get_absolute_url=permalink(_get_absolute_url)