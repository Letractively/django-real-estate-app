from django.db.models import Manager, Q

class SelectFieldManager(Manager):

	def all_enabled(self):
		return super(SelectFieldManager,self).all().filter(Q(logical_exclude=False))


