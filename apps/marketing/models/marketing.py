# -*- coding: utf-8 -*-
from datetime import datetime

from django import template
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
	template = "admin/marketing/marketingobject/marketingobject_rendered.html"

	class Meta:
		app_label           = 'marketing'
		db_table            = 'real_estate_app_apps_marketing_marketing'		
		get_latest_by       = 'pub_date'
		ordering            = ('-pub_date',)
		verbose_name        = _('Marketing')
		verbose_name_plural = _('Marketing')

	def _render_object(self):
		"""
			Render a MarketingObject to portlet
		"""
		import hexagonit.swfheader
		from django.utils.safestring import mark_safe
		from django.template.defaultfilters import slugify
		
		is_swf=False
		metadata={
			'url':self.files_fk.files.url,
			'class':slugify(self.title),
			'title':self.title,
		}

		try:
			metadata.update(hexagonit.swfheader.parse(self.files_fk.files.path))
			is_swf=True
		except ValueError:
			try:
				import Image
				image=Image.open(self.files_fk.files.path)
			except IOError:
				return mark_safe("""<p>%s</p>""" % _("[ERROR RENDER MARKETING]: Only suports Images and Flash files."))

		context=template.Context({
			'metadata':metadata,
			'files':self.files_fk,
			'obj':self,
			'is_swf':is_swf
		})

		return template.loader.get_template(self.template or [
                "admin/marketing/marketingobject_rendered.html",
                "admin/marketingobject_rendered.html"
        ]).render(context)

	render=property(_render_object)