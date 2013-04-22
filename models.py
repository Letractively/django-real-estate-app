# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

class RealEstateAppBaseModel(models.Model):

	logical_exclude = models.NullBooleanField(
					_('Logical exclude'),
					default=False,
					null=True,
					editable=False
	)

	enable_publish = models.BooleanField(
							_('Enable publish'), 
							default=True
	)

	create_date = models.DateTimeField(
							_('Creation date'),
							default=datetime.now(),
							help_text=_('Entry with a init of date publicashion')
	)
	
	class Meta:
		abstract       = True

class RealEstateAppCompleteModel(models.Model):

	title = models.CharField(
					_('Title'),
					max_length=255,
					blank=True,
					null=True
	)

	slug = models.SlugField(
					_('Slug'),
					unique=True
	)

	pub_date = models.DateField(
				default=datetime.now()
	)

	enable_publish = models.BooleanField(
							_('Enable publish'), 
							default=True
	)

	logical_exclude = models.NullBooleanField(
					_('Logical exclude'),
					default=False,
					null=True,
					editable=False
	)

	class Meta:
		abstract       = True
		get_latest_by  = 'pub_date'
		ordering       = ('-pub_date',)