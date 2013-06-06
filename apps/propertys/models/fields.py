# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.localflavor.br.br_states import STATE_CHOICES

from real_estate_app.models import RealEstateAppBaseModel
from real_estate_app.managers import RealEstateManager
from real_estate_app.apps.propertys.manager import DistrictSelectFieldManager


class District(RealEstateAppBaseModel):
	district=models.CharField(
						_('District'),
						max_length=100,
						help_text=_('Enter with new district.')

	)

	state = models.CharField(
					_('State'),
					choices=STATE_CHOICES,
					max_length=2,
					help_text=_('State of that belongs to district')
	)
					
	objects = DistrictSelectFieldManager() 

	def __unicode__(self):
		return u'%s - %s' % (self.district, self.state)

	class Meta:	
		app_label = 'propertys'
		db_table  = 'real_estate_app_apps_propertys_district'
		get_latest_by='district'
		ordering=('district',)
		verbose_name=_('District')
		verbose_name_plural=_('Districts')

	def _state(self):
		state=dict(STATE_CHOICES)
		return state.get(self.state) or ''

	state_name=property(_state)


class Classification(RealEstateAppBaseModel):
	classification=models.CharField(
					_('Classification'),
					max_length=100,
					help_text=_('Enter with new classification. Ex.: House, Build,...')
	)

	objects = RealEstateManager() 

	def __unicode__(self):
		return u'%s' % self.classification 

	class Meta:	
		app_label = 'propertys'
		db_table  = 'real_estate_app_apps_propertys_classification'
		get_latest_by='classification'
		ordering=('classification',)
		verbose_name=_('Classification')
		verbose_name_plural=_('Classifications')


class StatusProperty(RealEstateAppBaseModel):
	statusproperty=models.CharField(
					_('Status Property'),
					max_length=100,
					help_text=_('Enter with new status. Ex.: Rent, Sale,...')
	)
	
	objects = RealEstateManager() 

	def __unicode__(self):
		return self.statusproperty 

	class Meta:	
		app_label = 'propertys'
		db_table  = 'real_estate_app_apps_propertys_status_property'
		get_latest_by='statusproperty'
		ordering=('statusproperty',)
		verbose_name=_('Status Property')
		verbose_name_plural=_('Status Propertys')

class AditionalThings(RealEstateAppBaseModel):

	name=models.CharField(
						_('Name'),
						max_length=255,
						help_text=_('Enter with new aditional things to property. Ex.: Pool, Barbecue,...')
	)

#   TODO: report a bug to django about this error when i use the 
#	      CheckboxSelectMultiple with custom Manager has problem.
#         Not work with logical_exclude and mark all checked
	objects = RealEstateManager()

	def __unicode__(self):
		return self.name

	class Meta:	
		app_label = 'propertys'
		db_table  = 'real_estate_app_apps_propertys_aditionalthings'
		get_latest_by='name'
		ordering=('name',)
		verbose_name=_('Aditional things')
		verbose_name_plural=_('Aditionals things')

class PositionOfSun(RealEstateAppBaseModel):

	position=models.CharField(
						_('Position'),
						max_length=255,
						help_text=_('Enter with a new position of sun of a property.')
	)
	
	objects = RealEstateManager() 

	def __unicode__(self):
		return self.position 

	class Meta:	
		app_label = 'propertys'
		db_table  = 'real_estate_app_apps_propertys_position_of_sun'
		get_latest_by='position'
		ordering=('position',)
		verbose_name=_('Position of sun')
		verbose_name_plural=_('Positions of sun')