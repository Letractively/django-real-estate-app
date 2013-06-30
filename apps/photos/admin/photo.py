from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
 

from real_estate_app.apps.photos.models import Photo
from real_estate_app.apps.photos.admin.forms import PhotoAdminForm

class PhotoInlineAdmin(admin.StackedInline):

	prepopulated_fields = {'slug': ('photo',)}
	exclude=('create_date',)
	model = Photo
	extra = 0
	form = PhotoAdminForm 
	template = 'admin/photos/photo/edit_inline/stacked.html'
	fields = ('photo','slug','description','pub_date','image_destaque','enable_publish')

	def _media(self):
		from django.conf import settings
		from real_estate_app.conf.settings import MEDIA_REAL_ESTATE
		js = ['js/jquery.min.js', 'js/jquery.init.js']
		if self.prepopulated_fields:
			js.append('js/urlify.js')
			js.append('js/prepopulate.min.js')
		if self.filter_vertical or self.filter_horizontal:
			js.extend(['js/SelectBox.js' , 'js/SelectFilter2.js'])
		admin=['%s%s' % (settings.ADMIN_MEDIA_PREFIX, url) for url in js]
		admin.append('%s%s' %(MEDIA_REAL_ESTATE,'admin/js/custom-inlines.js'))
		admin.append('%s%s' %(MEDIA_REAL_ESTATE,'bootstrap2/plugins/bootstrap-tooltip.min.js'))
		admin_css={'all':['%s%s' %(MEDIA_REAL_ESTATE,'bootstrap2/plugins/bootstrap-tooltip.min.css')]}
		return forms.Media(js=admin,css=admin_css)
	media = property(_media)