from django.utils.translation import ugettext_lazy as _
from django.contrib import admin 
from real_estate_app.models import Images
from real_estate_app.forms.images import ImageAdminForm

class ImagesInlineAdmin(admin.StackedInline):

	prepopulated_fields = {"slug": ("images",)}
	model = Images
	extra = 1
	form = ImageAdminForm 
	template = 'admin/real_estate_app/edit_inline/stacked.html'

