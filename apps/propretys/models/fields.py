# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.br.br_states import STATE_CHOICES

from real_estate_app.managers import SelectFieldManager
from real_estate_app.apps.propretys.manager import DistrictSelectFieldManager


class District(models.Model):
	district=models.CharField(
						_('District'),
						max_length=100,
						help_text=_('Enter with new district.')

	)
	logical_exclude = models.NullBooleanField(
					_('Logical exclude'),
					default=False,
					editable=False,
					null=True
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
		app_label = 'propretys'
		db_table  = 'real_estate_app_apps_propretys_district'
		get_latest_by='district'
		ordering=('district',)
		verbose_name=_('District')
		verbose_name_plural=_('Districts')

	def _state(self):
		state=dict(STATE_CHOICES)
		return state.get(self.state) or ''

	state_name=property(_state)


class Classification(models.Model):
	classification=models.CharField(
					_('Classification'),
					max_length=100,
					help_text=_('Enter with new classification. Ex.: House, Build,...')
	)
	logical_exclude = models.NullBooleanField(
					_('Logical exclude'),
					default=False,
					editable=False,
					null=True
	)

	objects = SelectFieldManager() 

	def __unicode__(self):
		return self.classification 

	class Meta:	
		app_label = 'propretys'
		db_table  = 'real_estate_app_apps_propretys_classification'
		get_latest_by='classification'
		ordering=('classification',)
		verbose_name=_('Classification')
		verbose_name_plural=_('Classifications')


class StatusProprety(models.Model):
	statusproprety=models.CharField(
					_('Status Proprety'),
					max_length=100,
					help_text=_('Enter with new status. Ex.: Rent, Sale,...')
	)
	logical_exclude = models.NullBooleanField(
					_('Logical exclude'),
					default=False,
					null=True,
					editable=False
	)
	
	objects = SelectFieldManager() 

	def __unicode__(self):
		return self.statusproprety 

	class Meta:	
		app_label = 'propretys'
		db_table  = 'real_estate_app_apps_propretys_status_proprety'
		get_latest_by='statusproprety'
		ordering=('statusproprety',)
		verbose_name=_('Status Proprety')
		verbose_name_plural=_('Status Propretys')

class AditionalThings(models.Model):

	name=models.CharField(
						_('Name'),
						max_length=255,
						help_text=_('Enter with new aditional things to proprety. Ex.: Pool, Barbecue,...')
	)
	logical_exclude = models.NullBooleanField(
					_('Logical exclude'),
					default=False,
					null=True,
					editable=False
	)
#   TODO: report a bug to django about this error when i use the 
#	      CheckboxSelectMultiple with custom Manager has problem.
#         Not work with logical_exclude and mark all checked
#	objects = SelectFieldManager()

	def __unicode__(self):
		return self.name

	class Meta:	
		app_label = 'propretys'
		db_table  = 'real_estate_app_apps_propretys_aditionalthings'
		get_latest_by='name'
		ordering=('name',)
		verbose_name=_('Aditional things')
		verbose_name_plural=_('Aditionals things')

class PositionOfSun(models.Model):

	position=models.CharField(
						_('Position'),
						max_length=255,
						help_text=_('Enter with a new position of sun of a proprety.')
	)

	logical_exclude = models.NullBooleanField(
					_('Logical exclude'),
					default=False,
					null=True,
					editable=False
	)
	
	objects = SelectFieldManager() 

	def __unicode__(self):
		return self.position 

	class Meta:	
		app_label = 'propretys'
		db_table  = 'real_estate_app_apps_propretys_position_of_sun'
		get_latest_by='position'
		ordering=('position',)
		verbose_name=_('Position of sun')
		verbose_name_plural=_('Positions of sun')