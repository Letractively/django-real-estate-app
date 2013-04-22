from django.utils.translation import ugettext_lazy as _
from django.contrib import admin 
from real_estate_app.apps.real_estate_files.models import Files
from real_estate_app.conf.settings import MEDIA_PREFIX

class FilesAdmin(admin.ModelAdmin):

	search_fields=('title','files')

	fieldsets = (
		(_('files'), {
			'fields':['title','slug','pub_date','files',]
		}),
	)

	list_display=('title','pub_date','files',)
	prepopulated_fields = {'slug': ('files',)}
	class Media:
		css = {
			'all':(
					MEDIA_PREFIX+"css/tabs.css",
			),
		}
		js =(
		    MEDIA_PREFIX+'js/jquery.createtabs.js',
			MEDIA_PREFIX+"js/files-load.js",
		)

admin.site.register(Files, FilesAdmin)