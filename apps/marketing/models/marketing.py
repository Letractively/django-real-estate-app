# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

class MaketingObject(models.Model):

	title=models.CharField(
			_('Title'),	
			max_length=255,
			help_text=_('Entry the title of propaganda')
	)

	description=models.TextField(
			_('Description'),
			blank=True,
			null=True,
			help_text=_('Entry with description of propaganda')
	)

	enable_published = models.BooleanField(
			_('Enable publish'),
			default=True
	)

	files=models.ForeignKey(
		'real_estate_files.Files',
		blank=True,
		null=True,
		help_text=_('Entry with file of propaganda')
	)

	pub_date = models.DateField(
							_('Published date'),
							help_text=_('Entry with a publication date.'),
							default=datetime.now(),
	)

	date_init = models.DateField(
							_('Date of init published'),
							help_text=_('Entry with a init publication date')
	)

	date_end = models.DateField(
							_('Date of end published'),
							help_text=_('Entry with a end publication date')
	)

	def in_future(self):
		return self.pub_date > datetime.now()

	class Meta:
		app_label           = 'marketing'
		db_table            = 'real_estate_app_apps_marketing_marketing'		
		get_latest_by       = 'pub_date'
		ordering            = ('-pub_date',)
		verbose_name        = _('Marketing')
		verbose_name_plural = _('Marketing')
