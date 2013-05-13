from select_manager import SelectFieldManager

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

