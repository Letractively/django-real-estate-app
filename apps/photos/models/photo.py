# -*- coding: utf-8 -*-
import re, Image
from datetime import datetime
from os import path

from sorl.thumbnail import get_thumbnail

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink

from real_estate_app.models import RealEstateAppBaseModel
from real_estate_app.utils import radomstring 

GET_THUMB_PATTERN = re.compile(r'^get_photo_(\d+)x(\d+)_(thumb_url|thumb_filename|resize_url)$')
GET_THUMBNAIL = re.compile(r'get_(sorlthumbnail_crop)_(\d+)x(\d+)$')

def get_album(instance, filename):

	if instance.album_property is None:
		return 'real_estate_app/photos/'+datetime.now().strftime('%Y/%m/%d/')+filename
	else:
		return 'real_estate_app/photos/'+instance.album_property.slug+datetime.now().strftime('/%Y/%m/%d/')+filename

class Photo(RealEstateAppBaseModel):
	
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
		return '%s' % self.photo

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
		match = re.match(GET_THUMB_PATTERN, name)
		matchh = re.match(GET_THUMBNAIL,name)

		if match is None and matchh is None:
			raise AttributeError, name

		try:
			methodd, widthh, heightt = matchh.groups()

			def get_thumbnail_crop():
				my_file=self.photo.file.name
				size = widthh+'x'+heightt
				return get_thumbnail(my_file, size, crop='center', quality=99)

			if methodd == "sorlthumbnail_crop":
				return get_thumbnail_crop

		except AttributeError:
			pass
		### All others methods different of get_thumbnail_crop or get_thumbnail will
		### be deprecated.
		try: 
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
	
	def clean(self):
		"""
		Use clean because a slug is target as unique, and maybe user can add a photo with 
		same name.
		"""
		self.slug = '%s%s' %(self.slug, radomstring())
