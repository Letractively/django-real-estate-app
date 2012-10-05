from real_estate_app.models import Images 
from photo import PhotoAdminForm 

class ImageAdminForm(PhotoAdminForm):
	class Meta:
		model=Images
