from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Manager, Q

class PhotoManager(Manager):

		def published(self):
			try:
				qs = super(PhotoManager,self).get_query_set()
				return qs.filter(is_published=True)
			except ObjectDoesNotExist:
				return []