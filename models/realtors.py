# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from real_estate_app.models.others import Phone, Address
from real_estate_app.manager import SelectFieldManager

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

SEX=(
	(u'1',_('Male')),
	(u'2',_('Female')),
)

def get_realtor_directory(instance, filename):
		return 'real_estate_app/photos/realtor/'+instance.name+'/'+datetime.now().strftime('%Y/%m/%d/')+'/'+filename


class Realtor(models.Model):

	user = models.ForeignKey(User, unique=True)

	sex = models.CharField(
							_('Sex'),
							max_length=1,
							choices=SEX,
							blank=True
	)
	
	photo = models.ImageField(
							_('photo'),
							upload_to=get_realtor_directory,
							max_length=255,
							blank=True
	)

	logical_exclude = models.NullBooleanField(
					_('Logical exclude'),
					default=False,
					null=True,
					editable=False
	)

	if LANGUAGE_CODE in ('pt_BR','pt-br'):
		from django.contrib.localflavor.br.br_states import STATE_CHOICES
		from real_estate_app.localflavor.br import TIPO_PESSOA

		cpf = models.CharField(
								u'CPF',
								max_length=17,
								blank=True,
								unique=True
		)
	
		rg = models.CharField(
						   	u'RG',
						   	max_length=10,
						   	blank=True
		)
	
		ssp = models.CharField(
								u'SSP',
								max_length=2,
								choices=STATE_CHOICES,
								blank=True
		)

		cnpj = models.CharField(
							u'CNPJ',
							max_length=18,
							blank=True
		)

		razao_social=models.CharField(
							u'Razao Social',
							max_length=250,
							blank=True
		)

		tipo_pessoa = models.CharField(
							u'Pessoa Física ou Jurídica',
							max_length=3,
							choices=TIPO_PESSOA,
							default='PF'
		)

		creci = models.CharField(
							u'CRECI',
							max_length=10,
		)
	
	objects= SelectFieldManager()

	class Meta:
		app_label = 'real_estate_app'
		get_latest_by='username'
		ordering=('user',)
		verbose_name=_('Realtor')
		verbose_name_plural=_('Realtors')

	def __unicode__(self):

		if LANGUAGE_CODE in ('pt-br','pt_BR') and self.razao_social:
			return u'%s' % (self.razao_social)
				
		return u'%s' % self.name

	def get_first_name(self):
		try:
			return self.__name
		except AttributeError:
			try:
				self.__name = self.user.first_name
			except IndexError:
				self.__name = self.user.email
			return self.__name
	first_name=property(get_first_name)

	def get_last_name(self):
		try:
			return self.__name
		except AttributeError:
			try:
				self.__name = self.user.last_name
			except IndexError:
				self.__name = self.user.email
			return self.__name
	last_name=property(get_last_name)

	def get_user_name(self):
		try:
			return self.__name
		except AttributeError:
			try:
				self.__name = self.user.first_name+' '+self.user.last_name
			except IndexError:
				self.__name = self.user.email
			return self.__name
	name=property(get_user_name)

	def get_phones(self):
		try:
			return self.__phones
		except AttributeError:
			try:
				self.__phones = self.phones_set.all()
			except IndexError:
				self.__phones = None

			return self.__phones
	
	phones=property(get_phones)

	def get_email(self):
		try:
			return self.__email
		except AttributeError:
			try: 
				self.__email = self.user.email
			except IndexError:
				self.__email = None

			return self.__email
	email=property(get_email)

	def get_address(self):
		try:
			return self.__address
		except AttributeError:
			try:
				self.__address = self.address_set.all()
			except IndexError:
				self.__address = None

			return self.__address
	
	address=property(get_address)