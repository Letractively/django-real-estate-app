# -*- coding: utf-8 -*-
from datetime import datetime

from django.db.models import Manager, Q

class RealEstateManager(Manager):
	"""
		This Manager class required a model object has logical_exclude field.
	"""
	def all_enabled(self):
		return super(RealEstateManager,self).all().filter(Q(enable_publish=True), Q(logical_exclude=False))


class RealEstateCompleteModelManager(Manager):
	"""
		This Manager class required a model object has logical_exclude field.
	"""
	def all_enabled(self):
		qs = super(RealEstateCompleteModelManager,self).get_query_set().filter(Q(enable_publish=True), Q(logical_exclude=False))
		return qs.filter(Q(pub_date_end__gte=datetime.now())|Q(pub_date_end=None))