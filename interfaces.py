from django.contrib.auth.models import User
from django.db.models.fields import ForeignKey

class RealtorInterface(Object):
	
	def __init__(self,postinstance=None):
		self.instance=instance
		self.post=post
		

	def save(self,commit=True):
		return self.instance.save(commit)

