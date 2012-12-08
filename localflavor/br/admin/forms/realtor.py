# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

realtor_br_fieldsets= (
			(_('General Information'), {
				'fields': ('first_name','last_name','email','sex','photo','tipo_pessoa'),
			}),
			(_('Pessoa física'),{
				'fields': ('cpf','rg','ssp','creci')
			}),
			(_('Pessoa juridica'),{
				'fields': ('cnpj','razao_social','responsavel')
			})
)

realtor_br_custom_fields =('cpf','rg','ssp','creci','cnpj','razao_social','responsavel','tipo_pessoa')