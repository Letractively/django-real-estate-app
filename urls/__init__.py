from django.conf.urls.defaults import patterns 
from photo import photo_detail
from property import property_list, property_detail
from share import send_content
from feeds import feeds_property_url, feeds_news_url
from contact import contact 
from news import news_list, news_detail

urlpatterns = patterns('', contact, send_content, feeds_property_url, feeds_news_url, news_list, news_detail, property_list, photo_detail, property_detail)
