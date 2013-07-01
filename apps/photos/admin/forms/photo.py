from django import forms
from django.core.files.images import get_image_dimensions
from django.utils.translation import ugettext_lazy as _

from real_estate_app.apps.photos.models import Photo
from real_estate_app.conf.settings import MIN_HEIGHT, MIN_WIDTH
from real_estate_app.utils import radomstring
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

	def clean_slug(self):
		"""
		Use clean because a slug is target as unique, and maybe user can add a photo with 
		same name.
		"""
		from django.template.defaultfilters import slugify
		
		slug=self.cleaned_data.get('slug')
		try:
			photo_name=self.cleaned_data['photo']._name
			
			if slugify(photo_name) == slug:
				slug=u'%s%s' %(slug, radomstring())
		except AttributeError:
			pass

		return slug

	class Meta:
		model = Photo
