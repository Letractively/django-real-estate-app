from datetime import datetime

from django.db.models import Q

from real_estate_app.managers import RealEstateManager, RealEstateCompleteModelManager

class DistrictSelectFieldManager(RealEstateManager):

	def get_selected(self):
		qs = self.all_enabled()
		options={}
		for obj in qs:
			if not options.has_key(obj.state_name):
				options[obj.state_name]=[obj.district]
			else:
				options[obj.state_name].append(obj.district)

		return options

class PropertyManager(RealEstateCompleteModelManager):

		def all_destaque(self):
			return self.all_enabled().filter(Q(featured=True))