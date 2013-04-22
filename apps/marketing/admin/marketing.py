from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from real_estate_app.apps.marketing.models import MaketingObject
from real_estate_app.conf.settings import MEDIA_PREFIX

class MarketingObjectAdmin(admin.ModelAdmin):

	search_fields=('title','description','files')

	fieldsets = (
		(_('Marketing'), {
			'fields':['title','description','files',],
		}),
		(_('Published'),{
			'fields':['date_init','date_end','enable_published',],
		})
	)

	list_display=('title','date_init','date_end','enable_published')
	
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

admin.site.register(MaketingObject, MarketingObjectAdmin)
