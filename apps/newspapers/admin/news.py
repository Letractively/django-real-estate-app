from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from real_estate_app.admin.options import RealEstateAppPopUpModelAdmin
from real_estate_app.apps.newspapers.models import News
from real_estate_app.conf.settings import MEDIA_REAL_ESTATE


class NewsAdmin(RealEstateAppPopUpModelAdmin):
	search_fields = ['title']

	fieldsets = (
		(_('News'), {
			'fields':['title','content','slug'],
		}),
		(_('Publish'),{
			'fields':['enable_publish','pub_date','pub_date_end',],
		})
	)
	list_display = ('title','pub_date','pub_date_end','enable_publish')

	list_filter = ('enable_publish',)
	
	prepopulated_fields = {'slug': ('title',)}

	class Media:
		css = {
			'all':(
					MEDIA_REAL_ESTATE+"admin/css/facebox.css",
			),
		}
		js = (
			  MEDIA_REAL_ESTATE+'admin/js/tiny_mce/tiny_mce.js',
		      MEDIA_REAL_ESTATE+'admin/js/tiny_mce/textarea.js',
		      MEDIA_REAL_ESTATE+'admin/js/ajax_csrf.js',
			  MEDIA_REAL_ESTATE+'admin/js/facebox.js',
		)

admin.site.register(News,NewsAdmin)
