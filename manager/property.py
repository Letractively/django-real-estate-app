from datetime import datetime
from django.db.models import Manager, Q

class PropertyManager(Manager):

		def all_enabled(self):
			qs = super(PropertyManager,self).get_query_set().filter(enable_publish=True)
			return qs.filter(Q(date_end__gte=datetime.now())|Q(date_end=None))

		def all_destaque(self):
			return self.all_enabled().filter(Q(featured=True))

