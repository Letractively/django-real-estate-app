# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from real_estate_app.apps.visitcalendar.models import Visitor
from real_estate_app.models import RealEstateAppCompleteModel
from real_estate_app.managers import RealEstateManager
from real_estate_app.utils import RenderVariablesString

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

class TermVisit(RealEstateAppCompleteModel):

	text = models.TextField(
							_('Text of term'),
							blank=False,
							null=False,
							help_text=_('Term visit variables you can use: \n %s' % RenderVariablesString(
																						app='real_estate_app.apps.visitcalendar',
																						obj=Visitor
																					).str_variables_locale()
							)
	)

	objects = RealEstateManager()

	class Meta:
		app_label = 'visitcalendar'
		db_table  = 'real_estate_app_apps_visitcalendar_termvisit'
		get_latest_by='create_date'
		ordering=('create_date',)
		verbose_name=_('Term Visit')
		verbose_name_plural=_('Terms of hits')
