from django.db.models import Manager, Q

class SelectFieldManager(Manager):

	def all(self):
		qs = super(SelectFieldManager,self).get_query_set()
		return qs.filter(Q(logical_exclude=False))


