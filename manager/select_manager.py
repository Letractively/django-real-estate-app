from django.db.models import Manager, Q

class SelectFieldManager(Manager):

	def all(self):
		return super(SelectFieldManager,self).all().filter(Q(logical_exclude=False))


