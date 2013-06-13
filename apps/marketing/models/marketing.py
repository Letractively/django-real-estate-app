# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from real_estate_app.models import RealEstateAppCompleteModel

class MarketingObject(RealEstateAppCompleteModel):

	description=models.TextField(
			_('Description'),
			blank=True,
			null=True,
			help_text=_('Entry with description of propaganda')
	)

	files_fk=models.ForeignKey(
		'real_estate_files.Files',
		blank=True,
		null=True,
		help_text=_('Entry with file of propaganda')
	)

	class Meta:
		app_label           = 'marketing'
		db_table            = 'real_estate_app_apps_marketing_marketing'		
		get_latest_by       = 'pub_date'
		ordering            = ('-pub_date',)
		verbose_name        = _('Marketing')
		verbose_name_plural = _('Marketing')
