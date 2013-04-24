# -*- coding: utf-8 -*-
from django.conf import settings

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

FIELDS_LANGUAGE_CODE = { 'fields':('visitor_email',)}

if LANGUAGE_CODE in ('pt-br','pt_BR'):
	FIELDS_LANGUAGE_CODE= {
		'fields':('cpf',)
	}

VISITOR_SEARCH_FIELDS=FIELDS_LANGUAGE_CODE