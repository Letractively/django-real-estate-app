# -*- coding: utf-8 -*-
import re, Image
from datetime import datetime
from os import path

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from django.utils.translation import ugettext_lazy as _

from others import Phone, Address

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')
GET_THUMB_PATTERN = re.compile(r'^get_photo_(\d+)x(\d+)_(thumb_url|thumb_filename|resize_url)$')

SEXO=(
	(u'M',_('Masculino')),
	(u'F',_('Feminino')),
)

TIPO_PESSOA=(
	(u'PF',u'Pessoa Física'),
	(u'PJ',u'Pessoa Jurídica'),
)

def get_realtor_directory(instance, filename):
		return 'real_estate_app/photos/realtor/'+instance.name+'/'+datetime.now().strftime('%Y/%m/%d/')+'/'+filename


class Realtor(models.Model):

	user = models.ForeignKey(User, unique=True)

	if LANGUAGE_CODE in ('pt_BR','pt-br'):
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

		responsavel = models.CharField(
							u'Responsável',
							max_length=250,
							blank=True
		)

		tipo_pessoa = models.CharField(
							u'Pessoa Física ou Jurídica',
							max_length=3,
							choices=TIPO_PESSOA
		)

		creci = models.CharField(
							u'CRECI',
							max_length=10,
							blank=True
		)

	name = models.CharField(
							_('Name'),
							max_length=30,
							blank=True
	)

	last_name = models.CharField(
							_('Last name'),
							max_length=255,
							blank=True
	)

	sex = models.CharField(
							_('Sex'),
							max_length=1,
							choices=SEXO,
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
							
	class Meta:
		app_label = 'real_estate_app'
		get_latest_by='username'
		ordering=('name','last_name',)
		verbose_name=_('Realtor')
		verbose_name_plural=_('Realtors')

	def save(self):

		if LANGUAGE_CODE in ('pt_BR','pt-br'):
			if self.tipo_pessoa == 'PF':
				self.razao_social, self.cnpj, self.responsavel = '','',''
				self.username = self.cpf

			if self.tipo_pessoa == 'PJ':
				self.nome, self.sobrenome, self.cpf, self.rg, self.sexo = '','','','',''
				self.username = self.cnpj
		else:
			self.username = self.user.email 

		super(Realtor, self).save()

	def __unicode__(self):
		return u'%s %s' % (self.name, self.last_name)

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

	# def __getattr__(self, name):
	# 	"""
	# 	## This code is from django-fleshin
	# 	Deploys dynamic methods for on-demand thumbnails creation with any
	# 	size.

	# 	Syntax::

	# 	get_image_[WIDTH]x[HEIGHT]_[METHOD]

	# 	Where *WIDTH* and *HEIGHT* are the pixels of the new thumbnail and
	# 	*METHOD* can be ``url`` or ``filename``.

	# 	Example usage::

	#     >>> user = UserProfile(foto="/tmp/example.jpg", ...)
	#     >>> user.save()
	#     >>> user.get_image_320x240_url()
	#     >>> u"http://media.example.net/images/2008/02/26/example_320x240.jpg"
	#     >>> user.get_image_320x240_filename()
	#     >>> u"/srv/media/images/2008/02/26/example_320x240.jpg"
	# 	"""
	# 	match = re.match(GET_THUMB_PATTERN, name)

	# 	width, height, method = match.groups()
	# 	size = int(width), int(height)

	# 	def get_image_thumbnail_filename():
	# 		file, ext = path.splitext(self.photo.file.name)
	# 		print file
	# 		return file + '_%sx%s' % size + ext

	# 	def get_image_thumbnail_url():
	# 		url, ext = path.splitext(self.photo.url)
	# 		return url + '_%sx%s' % size + ext

	# 	thumbnail = get_image_thumbnail_filename()
	# 	if not path.exists(thumbnail):
	# 		img = Image.open(self.photo.file.name)
	# 		img.thumbnail(size, Image.ANTIALIAS)
	# 		img.save(thumbnail)

	# 	if method == "url":
	# 		return get_image_thumbnail_url
	# 	elif method == "filename":
	# 		return get_image_thumbnail_filename