# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from real_estate_app.managers import RealEstateManager, RealEstateCompleteModelManager

class RealEstateAppBaseModel(models.Model):
	def __init__(self,*args, **kwargs):
		super(RealEstateAppBaseModel,self).__init__(*args,**kwargs)
		self.template = "admin/%s/%s/%s_rendered.html" % (self._meta.app_label,self._meta.object_name.lower(),self._meta.object_name.lower())


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

	objects = RealEstateManager()
	
	class Meta:
		abstract = True

	def _render_object(self):
		"""
			Render a object to portlet
		"""
		from django import template
		object_name=self._meta.object_name.lower()
		app_label=self._meta.app_label

		context=template.Context({
			'obj':self,
		})
		
		return template.loader.get_template(self.template or [
                "admin/%s/%s_rendered.html" % (app_label,object_name),
                "admin/%s_rendered.html" % object_name
        ]).render(context)

	render=property(_render_object)


class RealEstateAppCompleteModel(models.Model):

	def __init__(self,*args, **kwargs):
		super(RealEstateAppCompleteModel,self).__init__(*args,**kwargs)
		self.template = "admin/%s/%s/%s_rendered.html" % (self._meta.app_label,self._meta.object_name.lower(),self._meta.object_name.lower())

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
				_('Date init'),
				default=datetime.now()
	)

	pub_date_end = models.DateField(
				_('Date end'),
				null=True,
				blank=True,
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

	logical_exclude = models.NullBooleanField(
					_('Logical exclude'),
					default=False,
					null=True,
					editable=False
	)

	objects = RealEstateCompleteModelManager()


	def in_future(self):
		return self.pub_date > datetime.now()

	def __unicode__(self):
		return u'%s' % self.title

	class Meta:
		abstract       = True
		get_latest_by  = 'pub_date'
		ordering       = ('-pub_date',)

	def _render_object(self):
		"""
			Render a object to portlet
		"""
		from django import template
		object_name=self._meta.object_name.lower()
		app_label=self._meta.app_label

		context=template.Context({
			'obj':self,
		})
		
		return template.loader.get_template(self.template or [
                "admin/%s/%s_rendered.html" % (app_label,object_name),
                "admin/%s_rendered.html" % object_name
        ]).render(context)

	render=property(_render_object)