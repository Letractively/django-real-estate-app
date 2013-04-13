from django.db import models
from django.utils.translation import ugettext_lazy as _

class PlaceMarkitingImage(models.Model):

	title=models.CharField(
			_('Title'),	
			max_length=255,
			help_text=_('Entry the title of propaganda')

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

