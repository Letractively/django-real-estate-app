# -*- coding: utf-8 -*-
from real_estate_app.conf.settings import MANAGERS, REAL_ESTATE_EMAIL 
from real_estate_app.apps.visitcalendar.messages import msg_new_visit_event, subtitle_new_visit_event
from real_estate_app.apps.visitcalendar.models import VisitEvent
from real_estate_app.utils import alertemail 
from django.db.models.signals import post_save

def signal_alertemail(sender,instance, **kwargs):
	if kwargs.get('created',False) and instance:
		MANAGERS_EMAILS=[mail_tuple[1] for mail_tuple in MANAGERS]
		alertemail(instance,subtitle_new_visit_event, msg_new_visit_event, REAL_ESTATE_EMAIL, MANAGERS_EMAILS, 
			       fields=['visitor_fk','date_visit','property_fk','get_absolute_url'])

post_save.connect(signal_alertemail,sender=VisitEvent)