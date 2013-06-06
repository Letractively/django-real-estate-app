from django.utils.translation import ugettext_lazy as _
from django.contrib import admin 

from real_estate_app.admin.options import RealEstateAppPopUpModelAdmin
from real_estate_app.apps.real_estate_files.models import Files
from real_estate_app.conf.settings import MEDIA_PREFIX

class FilesAdmin(RealEstateAppPopUpModelAdmin):

	search_fields=('title','files')

	fieldsets = (
		(_('files'), {
			'fields':['title','slug','files',]
		}),
		(_('Published'),{
			'fields':['pub_date','enable_publish',],
		}),
	)

	list_display=('title','pub_date','files','enable_publish')
	prepopulated_fields = {'slug': ('files','title')}


admin.site.register(Files, FilesAdmin)