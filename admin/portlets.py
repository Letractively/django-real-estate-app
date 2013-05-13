from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from real_estate_app.conf.settings import MEDIA_PREFIX
from real_estate_app.models import PortletPropagandaImage
from real_estate_app.admin import PropertyAdmin
from images import ImagesInlineAdmin 

class PortletPropagandaImageAdmin(admin.ModelAdmin):
	search_fields = ['title']

	fieldsets = (
		(_('Portlet image'), {
			'fields':['title','slug','link_images','description'],
		}),
		(_('Publish'),{
			'fields':['enable_published','date_init','date_end'],
		})
	)
	list_display = ('title','enable_published','date_init','date_end')

	list_filter = ('enable_published',)
	
	prepopulated_fields = {'slug': ('title',)}

	inlines = (
			ImagesInlineAdmin,
	)

	class Media:
		css = {
			'all':(
					MEDIA_PREFIX+"css/facebox.css",
					MEDIA_PREFIX+"css/tabs.css",
			),
		}
		js = (
			  MEDIA_PREFIX+'js/tiny_mce/tiny_mce.js',
		      MEDIA_PREFIX+'js/tiny_mce/textarea.js',
		      MEDIA_PREFIX+'js/ajax_csrf.js',
		      MEDIA_PREFIX+'js/jquery.createtabs.js',
		      MEDIA_PREFIX+'js/load.js',
			  MEDIA_PREFIX+'js/facebox.js',
		      MEDIA_PREFIX+'js/images.js',
		)

admin.site.register(PortletPropagandaImage,PortletPropagandaImageAdmin)
