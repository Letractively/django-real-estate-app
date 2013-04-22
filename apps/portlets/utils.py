from django.db.models.loading import get_model

def get_portlet_model(type_portlet):
	try:
		apps,models=type_portlet.split('.')
		return get_model(apps,models)
	except:
		return None