from django.conf.urls.defaults import patterns 

from share import send_content
from contact import contact 

from real_estate_app.apps.propertys.urls import property_list, property_detail, feeds_property_url, property_sitemap
from real_estate_app.apps.photos.urls import photo_detail
from real_estate_app.apps.newspapers.urls import newspapers_list, newspapers_detail, newspapers_sitemap, feeds_newspapers_url
from real_estate_app.apps.portlets.urls import portlet_edit, portlet_create
from real_estate_app.apps.visitcalendar.urls import visitcalendar_list_json, visitcalendar_list_json_index, visitcalendar_list, visitcalendar_list_property_visit, visitcalendar_create_object, visitcalendar_update_object

urlpatterns = patterns('', 
						contact, send_content, 
						feeds_newspapers_url, newspapers_list, newspapers_detail, 
					    portlet_edit, portlet_create, 
					    visitcalendar_list_json, visitcalendar_list_json_index, visitcalendar_list_property_visit, visitcalendar_list, visitcalendar_create_object, visitcalendar_update_object,
					    property_list, photo_detail, property_detail, property_sitemap, feeds_property_url,
			   )
