# -*- coding: utf-8 -*-
import re, Image
from datetime import datetime
from os import path

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from real_estate_app.managers import RealEstateManager
from real_estate_app.models import RealEstateAppBaseModel

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

SEX=(
	(u'1',_('Male')),
	(u'2',_('Female')),
)

GET_THUMB_PATTERN = re.compile(r'^get_photo_(\d+)x(\d+)_(thumb_url|thumb_filename|resize_url)$')

def get_realtor_directory(instance, filename):
		return 'real_estate_app/photos/realtor/'+instance.name+'/'+datetime.now().strftime('%Y/%m/%d/')+'/'+filename


class Realtor(RealEstateAppBaseModel):

	user = models.ForeignKey(User, unique=True)

	sex = models.CharField(
							_('Sex'),
							max_length=1,
							choices=SEX,
							blank=True
	)

	phone = models.CharField(
							_('Phone'),
							max_length=20,
							blank=True
	)

	celphone = models.CharField(
							_('Celphone'),
							max_length=20,
							blank=True
	)
	
	photo = models.ImageField(
							_('photo'),
							upload_to=get_realtor_directory,
							max_length=255,
							blank=True
	)

	if LANGUAGE_CODE in ('pt_BR','pt-br'):
		from django.contrib.localflavor.br.br_states import STATE_CHOICES
		from real_estate_app.localflavor.br import TIPO_PESSOA

		cpf = models.CharField(
								u'CPF',
								max_length=14,
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
	
	objects= RealEstateManager()

	class Meta:
		app_label = 'realtors'
		db_table  = 'real_estate_app_apps_realtors_realtor'
		get_latest_by='username'
		ordering=('user',)
		verbose_name=_('Realtor')
		verbose_name_plural=_('Realtors')
		
		if LANGUAGE_CODE in ('pt_BR','pt-br'):
			unique_together=[('rg','ssp'),('creci','ssp')]


	def __unicode__(self):
				
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
		if LANGUAGE_CODE == 'pt-br' and self.tipo_pessoa == 'PJ':
			self.__name=self.razao_social
			return self.__name
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


	def __getattr__(self, name):
		"""
		Deploys dynamic methods for on-demand thumbnails creation with any
		size.

		Syntax::

		get_photo_[WIDTH]x[HEIGHT]_[METHOD]

		Where *WIDTH* and *HEIGHT* are the pixels of the new thumbnail and
		*METHOD* can be ``url`` or ``filename``.

		Example usage::

	    >>> photo = Photo(photo="/tmp/example.jpg", ...)
	    >>> photo.save()
	    >>> photo.get_photo_320x240_url()
	    >>> u"http://media.example.net/photos/2008/02/26/example_320x240.jpg"
	    >>> photo.get_photo_320x240_filename()
	    >>> u"/srv/media/photos/2008/02/26/example_320x240.jpg"
		"""
		match = re.match(GET_THUMB_PATTERN, name)
		if match is None:
			raise AttributeError, name
		width, height, method = match.groups()
		size = int(width), int(height)

		def get_photo_thumbnail_filename():
			file, ext = path.splitext(self.photo.file.name)
			return file + '_%sx%s' % size + ext

		def get_photo_thumbnail_url():
			url, ext = path.splitext(self.photo.url)
			return url + '_%sx%s' % size + ext	


		def get_photo_thumbnail_resize_filename():
			file, ext = path.splitext(self.photo.file.name)
			return file + '_%sx%s_' % size + method + ext

		def get_photo_thumbnail_resize_url():
			url, ext = path.splitext(self.photo.url)
			return url + '_%sx%s_' % size + method + ext	

		if method == "thumb_url" or method=="thumb_filename":	
			thumbnail = get_photo_thumbnail_filename()
		else:
			thumbnail = get_photo_thumbnail_resize_filename()

		if not path.exists(thumbnail):
			img = Image.open(self.photo.file.name)

			if method =="thumb_url" or method == "thumb_filename":
				img.thumbnail(size, Image.ANTIALIAS)
				img.save(thumbnail)
			else:
				(img_width,img_height)=img.size
				
				wpercent=(size[0]/float(img_width))
				HSIZE=int((float(img_height)*float(wpercent)))

				y_crop=int((float((HSIZE/2.0))-float((size[1]/2.0))))
				height_crop=(HSIZE-y_crop)				
				
				box=(0,y_crop,size[0],height_crop)

				new_img = img.resize((size[0],HSIZE),Image.ANTIALIAS)

				crop=new_img.crop(box)
				crop.load()
				crop.save(thumbnail)

		if method == "thumb_url":
			return get_photo_thumbnail_url
		elif method == "resize_url":
			return get_photo_thumbnail_resize_url
		else:
			return get_photo_thumbnail_filename