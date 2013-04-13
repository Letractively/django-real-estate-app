# -*- conding: utf-8; -*-
import re, Image
from os import path

from datetime import datetime 
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.db import models

from real_estate_app.models import PortletPropagandaImage

GET_THUMB_PATTERN = re.compile(r'^get_image_(\d+)x(\d+)_(thumb_url|thumb_filename|resize_url)$')

def get_portlets_images(instance, filename):
		if instance.portletpropagandaimage is None:
			return 'real_estate_app/portlets/images/'+datetime.now().strftime('%Y/%m/%d/')+filename
		else:
			return 'real_estate_app/images/'+instance.portletpropagandaimage.slug+datetime.now().strftime('/%Y/%m/%d/')+filename

class Images(models.Model):
	
	portletpropagandaimage=models.ForeignKey(
		PortletPropagandaImage
	)
	slug = models.SlugField(
			        _('slug'),
			        unique=True,
			        help_text=_('Automatically built from the caption. A slug is a short label generally used in URLs.')
	)

	pub_date = models.DateTimeField(
			    _('date published'),
		        default=datetime.now,
		        help_text=_('Files in future dates are only published on \
		                     correct date.'),
	)
	
	images=models.ImageField(
			_('Images'),
			upload_to=get_portlets_images
	)
	
	def __unicode__(self):
		return u'%s: %s' %(self.portletpropagandaimage, self.images)

	class Meta:
		app_label = 'real_estate_app'
		get_latest_by = 'pub_date'
		ordering      = ('-pub_date',)
		verbose_name  = _('Image')
		verbose_name_plural = _('Images')

	def __getattr__(self, name):
		"""
		Deploys dynamic methods for on-demand thumbnails creation with any
		size.

		Syntax::

		get_image_[WIDTH]x[HEIGHT]_[METHOD]

		Where *WIDTH* and *HEIGHT* are the pixels of the new thumbnail and
		*METHOD* can be ``url`` or ``filename``.

		Example usage::

	    >>> image = image(image="/tmp/example.jpg", ...)
	    >>> image.save()
	    >>> image.get_image_320x240_url()
	    >>> u"http://media.example.net/images/2008/02/26/example_320x240.jpg"
	    >>> image.get_image_320x240_filename()
	    >>> u"/srv/media/images/2008/02/26/example_320x240.jpg"
		"""
		match = re.match(GET_THUMB_PATTERN, name)
		if match is None:
			raise AttributeError, name
		width, height, method = match.groups()
		size = int(width), int(height)

		def get_image_thumbnail_filename():
			file, ext = path.splitext(self.images.file.name)
			return file + '_%sx%s' % size + ext

		def get_image_thumbnail_url():
			url, ext = path.splitext(self.images.url)
			return url + '_%sx%s' % size + ext	


		def get_image_thumbnail_resize_filename():
			file, ext = path.splitext(self.images.file.name)
			return file + '_%sx%s_' % size + method + ext

		def get_image_thumbnail_resize_url():
			url, ext = path.splitext(self.images.url)
			return url + '_%sx%s_' % size + method + ext	

		if method == "thumb_url" or method=="thumb_filename":	
			thumbnail = get_image_thumbnail_filename()
		else:
			thumbnail = get_image_thumbnail_resize_filename()

		if not path.exists(thumbnail):
			img = Image.open(self.images.file.name)

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
			return get_image_thumbnail_url
		elif method == "resize_url":
			return get_image_thumbnail_resize_url
		else:
			return get_image_thumbnail_filename

	@permalink
	def get_absolute_url(self):
		return ('images-portlets', None, {
										'portletimage': str(self.portletpropagandaimage),
										'slug' : str(self.slug),
				})

	def in_future(self):
		return self.pub_date > datetime.now()
