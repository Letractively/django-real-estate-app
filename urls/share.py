from django.conf.urls.defaults import url

send_content = url(
	regex  = '^send-content/$',
	view   = 'real_estate_app.views.send_content',
	name   = 'share-send-content'
)
