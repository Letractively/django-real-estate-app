from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from real_estate_app.admin.options import RealEstateAppPopUpModelAdmin
from real_estate_app.apps.marketing.models import MarketingObject
from real_estate_app.conf.settings import MEDIA_PREFIX as MEDIA_PREFIX_REAL_ESTATE

class MarketingObjectAdmin(RealEstateAppPopUpModelAdmin):

	search_fields=('title','description','files_fk')

	fieldsets = (
		(_('Marketing'), {
			'fields':['title','description','files_fk',],
		}),
		(_('Publish'),{
			'fields':['pub_date','pub_date_end','enable_publish',],
		})
	)

	list_display=('title','pub_date','pub_date_end','enable_publish',)

	class Media:
		css = {
			'all':(
				MEDIA_PREFIX_REAL_ESTATE+"admin/css/facebox.css",
			)
		}
		js = (
				MEDIA_PREFIX_REAL_ESTATE+"admin/js/facebox.js",
				MEDIA_PREFIX_REAL_ESTATE+'admin/js/tiny_mce/tinymce.min.js',
		      	MEDIA_PREFIX_REAL_ESTATE+'admin/js/tiny_mce/textarea.js',
		      	MEDIA_PREFIX_REAL_ESTATE+'admin/js/ajax_csrf.js',
		)

admin.site.register(MarketingObject, MarketingObjectAdmin)
