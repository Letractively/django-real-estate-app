from django import forms
from django.core.files.images import get_image_dimensions
from django.utils.translation import ugettext_lazy as _
from real_estate_app.models import Photo
from real_estate_app.conf.settings import MIN_HEIGHT, MIN_WIDTH

class PhotoAdminForm(forms.ModelForm):

	
	def clean_photo(self):

		img=self.cleaned_data.get('photo')

		if not img:
			raise forms.ValidationError(_("No image!"))
		else:
			width,height=get_image_dimensions(img)

		#if image_destaque is True and ( int(width) < int(MIN_WIDTH) or int(height) < int(MIN_HEIGHT)) is True:
		#	raise forms.ValidationError(_("The image mark like a highlights must be %(width)sx%(height)s larger!") % {'width':str(MIN_WIDTH),'height':str(MIN_HEIGHT)} )
		return img

	class Meta:
		model = Photo
