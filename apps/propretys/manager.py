from datetime import datetime
from django.db.models import Manager, Q
from real_estate_app.managers.select_manager import SelectFieldManager

class DistrictSelectFieldManager(SelectFieldManager):

	def get_selected(self):
		qs = super(SelectFieldManager,self).get_query_set()
		options={}
		for obj in qs:
			if not options.has_key(obj.state_name):
				options[obj.state_name]=[obj.district]
			else:
				options[obj.state_name].append(obj.district)

		return options

class PropretyManager(Manager):

		def all_enabled(self):
			qs = super(PropretyManager,self).get_query_set().filter(enable_publish=True)
			return qs.filter(Q(date_end__gte=datetime.now())|Q(date_end=None))

		def all_destaque(self):
			return self.all_enabled().filter(Q(featured=True))