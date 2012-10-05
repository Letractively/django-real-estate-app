from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

class PortletPropagandaImage(models.Model):

	title=models.CharField(
			_('Title'),	
			max_length=255,
			help_text=_('Entry the title of propaganda')
	)

	slug = models.SlugField(
			_('slug'),
			unique=True,
			help_text=_('Automatically built from the caption. A slug is a short label generally used in URLs.')
	)

	link_images = models.CharField(
			_('Link'),
			max_length=255,
			help_text=_('Entry the link of propaganda')
	)

	description=models.TextField(
			_('Description'),
			blank=True,
			null=True,
			help_text=_('Entry with description of propaganda')
	)


	enable_published = models.BooleanField(
			_('Enable publish'),
			default=True
	)

	date_init = models.DateField(
							_('Date of init published'),
							help_text=_('Entry with a init of date publicashion')
	)

	date_end = models.DateField(
							_('Date of end published'),
							help_text=_('Entry with a end of date publicashion')
	)

	pub_date = models.DateTimeField(
			    _('date published'),
		        default=datetime.now,
		        help_text=_('Files in future dates are only published on \
		                     correct date.'),
	)

	def __unicode__(self):
		return u'%s' % self.title 

	class Meta:
		app_label     ='real_estate_app'
		get_latest_by = 'pub_date'    
		ordering      = ('-pub_date',)
		verbose_name  = _('Portlet Image')
		verbose_name_plural  = _('Portlet Images')
	
	def _get_images(self):
		images = self.images_set.all()
		if images:
			return images.order_by('?')

		return None

	images=property(_get_images)

	def get_random_image(self):
		queryset = self.images_set.all()
		if queryset:
			return queryset.order_by('?')[0]
		return None

