from django.db.models import Manager, Q

class SelectFieldManager(Manager):
	"""
		This Manager class required a model object has logical_exclude field.
	"""
	def all_enabled(self):
		return super(SelectFieldManager,self).all().filter(Q(logical_exclude=False))


