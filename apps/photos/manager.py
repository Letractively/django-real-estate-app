from django.core.exceptions import ObjectDoesNotExist

from real_estate_app.managers import RealEstateManager

class PhotoManager(RealEstateManager):

	def published(self):
		try:
			qs = super(PhotoManager,self).get_query_set()
			return qs.filter(enable_publish=True)
		except ObjectDoesNotExist:
			return []
