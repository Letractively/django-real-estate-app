from django import forms
from django.core.files.images import get_image_dimensions
from django.utils.translation import ugettext_lazy as _

from real_estate_app.apps.photos.models import Photo
from real_estate_app.conf.settings import MIN_HEIGHT, MIN_WIDTH
from real_estate_app.widgets import ImageInputWidget

class PhotoAdminForm(forms.ModelForm):

	photo = forms.FileField(
		label=_('Photo'),
		widget=ImageInputWidget(width=300,height=300),
	)
	
	def clean_photo(self):

		img=self.cleaned_data.get('photo')

		if not img:
			raise forms.ValidationError(_("No image!"))
		else:
			width,height=get_image_dimensions(img)
		return img

	class Meta:
		model = Photo
