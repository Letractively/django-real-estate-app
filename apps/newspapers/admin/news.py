from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from real_estate_app.conf.settings import MEDIA_PREFIX
from real_estate_app.apps.newspapers.models import News

class NewsAdmin(admin.ModelAdmin):
	search_fields = ['title']

	fieldsets = (
		(_('News'), {
			'fields':['title','content', 'link','slug'],
		}),
		(_('Publish'),{
			'fields':['enable_publish','pub_date'],
		})
	)
	list_display = ('title','pub_date','enable_publish')

	list_filter = ('enable_publish',)
	
	prepopulated_fields = {'slug': ('title',)}

	class Media:
		css = {
			'all':(
					MEDIA_PREFIX+"css/facebox.css",
					MEDIA_PREFIX+"css/tabs.css",
					MEDIA_PREFIX+"css/change-list.css",
			),
		}
		js = (
			  MEDIA_PREFIX+'js/tiny_mce/tiny_mce.js',
		      MEDIA_PREFIX+'js/tiny_mce/textarea.js',
		      MEDIA_PREFIX+'js/ajax_csrf.js',
		      MEDIA_PREFIX+'js/jquery.createtabs.js',
		      MEDIA_PREFIX+'js/load.js',
			  MEDIA_PREFIX+'js/facebox.js',
		)

admin.site.register(News,NewsAdmin)
