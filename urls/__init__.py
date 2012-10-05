from django.conf.urls.defaults import patterns 
from photo import photo_detail
from property import property_list,property_detail
from share import send_content
from feeds import feeds_url
from contact import contact 

urlpatterns = patterns('',contact, send_content, feeds_url, property_list, photo_detail, property_detail)
