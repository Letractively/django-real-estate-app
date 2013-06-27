from django.utils.translation import ugettext_lazy as _

fields_visitor_form=['cpf','first_name','last_name','rg','ssp','address','zip','celphone', 'email', 'phone', 'work_address','work_zip','work_phone']
fieldsets_visitor_form = {
	'general-information': ['cpf','rg','ssp'],
}