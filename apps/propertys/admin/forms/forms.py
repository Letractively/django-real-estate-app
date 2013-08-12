from django.forms import ChoiceField, ModelForm

from beermarket.widgets import StateDistrictAdminSelect

class SubsidiaryAdminForm(ModelForm):
	state = ChoiceField(
						label=_('State'),
						widget=StateDistrictAdminSelect,
						choices=STATE_CHOICES,
						initial='DF',
	)

