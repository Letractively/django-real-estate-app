from django.contrib import admin
from real_estate_app.views.popup import popup_add, popup_edit_delete
from real_estate_app.views.ajax import ajax_view_model

admin.site.index_template='admin/index-custom.html'