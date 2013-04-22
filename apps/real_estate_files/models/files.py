# -*- conding: utf-8; -*-
from datetime import datetime 

from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.db import models

def get_files(instance, filename):
		if instance is None:
			return 'real_estate_app/real_estate_files/'+datetime.now().strftime('%Y/%m/%d/')+filename
		else:
			return 'real_estate_app/real_estate_files/'+instance.slug+datetime.now().strftime('/%Y/%m/%d/')+filename

class Files(models.Model):

	title = models.CharField(
				max_length=255
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
	
	files=models.FileField(
			_('Files'),
			upload_to=get_files
	)
	
	def __unicode__(self):
		return u'%s' % self.files

	class Meta:
		app_label           = 'real_estate_files'
		db_table            = 'real_estate_app_apps_real_estate_files_files'
		get_latest_by       = 'pub_date'
		ordering            = ('-pub_date',)
		verbose_name        = _('file')
		verbose_name_plural = _('files')
	
	@permalink
	def get_absolute_url(self):
		return ('real_estate_files-files', None, {
					'slug' : str(self.slug),
				})

	def in_future(self):
		return self.pub_date > datetime.now()
