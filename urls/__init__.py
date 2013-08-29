from django.conf import settings
from django.conf.urls.defaults import patterns 

from share import send_content
from contact import contact 

from real_estate_app.apps.propertys.urls import property_list, property_detail, feeds_property_url, property_sitemap
from real_estate_app.apps.photos.urls import photo_detail
from real_estate_app.apps.newspapers.urls import newspapers_list, newspapers_detail, newspapers_sitemap, feeds_newspapers_url
from real_estate_app.apps.portlets.urls import portlet_edit, portlet_create
from real_estate_app.apps.visitcalendar.urls import visitcalendar_list_json, visitcalendar_list_json_day, visitcalendar_list_json_index, visitcalendar_list,\
													visitcalendar_list_property_visit, visitcalendar_create_object, visitcalendar_update_object,\
													visitcalendar_visitor_ajax_view

from real_estate_app.apps.visitclick.urls import visitclick_data_json_view

urlpatterns = patterns('',
		contact, send_content, 
		#newspapers
		newspapers_list, feeds_newspapers_url, newspapers_detail, 
		#portlets
		portlet_edit, portlet_create,
		#visitcalendar
		visitcalendar_list_json, visitcalendar_list_json_day, visitcalendar_list_json_index, visitcalendar_list_property_visit, 
		visitcalendar_list, visitcalendar_create_object, visitcalendar_update_object, visitcalendar_visitor_ajax_view,
		#visitclick
		visitclick_data_json_view,
		#propertys
		property_list,feeds_property_url, photo_detail, property_detail, property_sitemap,
		

)