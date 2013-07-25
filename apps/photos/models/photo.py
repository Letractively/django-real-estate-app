# -*- coding: utf-8 -*-
import re, Image
from datetime import datetime
from os import path

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink

from real_estate_app.models import RealEstateAppBaseModel
from real_estate_app.conf.settings import REAL_ESTATE_PROPERTY_UNKNOW_IMG

GET_THUMBNAIL = re.compile(r'get_(sorlthumbnail_crop)_(\d+)x(\d+)$')

def get_album(instance, filename):

	if instance.album_property is None:
		return 'real_estate_app/photos/'+datetime.now().strftime('%Y/%m/%d/')+filename
	else:
		return 'real_estate_app/photos/'+instance.album_property.slug+datetime.now().strftime('/%Y/%m/%d/')+filename

class Photo(RealEstateAppBaseModel):

	unknow_img=REAL_ESTATE_PROPERTY_UNKNOW_IMG
	
	album_property = models.ForeignKey(
		 'propertys.Property',
	     verbose_name=_('photos'), 
	)

	photo = models.ImageField(
        _('photo'),
		max_length=255,
        upload_to=get_album,
        width_field='width',
        height_field='height'
    )

	width = models.SmallIntegerField(_('width'), editable=False)
	height = models.SmallIntegerField(_('height'), editable=False)
	slug = models.SlugField(
        _('slug'),
		max_length=255,
        help_text=_('Automatically built from the caption. A slug is a short '
                    'label generally used in URLs.'),
    )

	description = models.CharField(
			_('Description of photo'),
			max_length=255,
			blank=True,
			null=True
	)

	pub_date = models.DateTimeField(
					    _('date published'),
				        default=datetime.now,
				        help_text=_('Photos in future dates are only published on \
				                    correct date.'),
    )

	image_destaque = models.BooleanField(
						u'Imagem destaque', 
			            default=False,
		                help_text=u'A imagem destaque aparecera na \
						           pagina inicial')

	def __unicode__(self):
		return u'%s' % self.photo

	class Meta:
		app_label = 'photos'
		db_table  = 'real_estate_app_apps_photos_photo'
		get_latest_by = 'pub_date'
		ordering      = ('-pub_date',)
		verbose_name  = _('photo')
		verbose_name_plural = _('photos')


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
		match = re.match(GET_THUMBNAIL,name)

		if match is None:
			raise AttributeError, name

		try:
			method, width, height = match.groups()

			def get_thumbnail_crop():
				from sorl.thumbnail import get_thumbnail
				size=width+'x'+height
				attrs={
					'crop':'center',
					'quality':99,
				}

				try:
					my_file=self.photo.file.name
				except ValueError:
					# TODO: discover why get error when try to pass 
					#       self.unknow_img to get_thumbnail
					return self.unknow_img
				
				return get_thumbnail(my_file,size, **attrs).url

			if method == "sorlthumbnail_crop":
				return get_thumbnail_crop

		except AttributeError:
			pass

	@permalink
	def get_absolute_url(self):
		return ('apps-photos', None, {
				'album': str(self.album_property.slug),
				'slug' : str(self.slug),
				})

	def in_future(self):
		return self.pub_date > datetime.now()