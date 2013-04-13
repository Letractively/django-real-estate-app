from django.forms import ModelForm

from real_estate_app.conf.settings import MEDIA_PREFIX

class PopUpModelForm(ModelForm):

	class Media:
 		css = {
			'all':[
				MEDIA_PREFIX+"css/popup.css",
			]
		}

		js = [
			"/admin-media/js/jquery.min.js",
			"/admin-media/js/jquery.init.js",
			#MEDIA_PREFIX+"js/real_estate_app_popup.js",
			MEDIA_PREFIX+"js/locale/pt_BR/realtor.js"
		]