from django.core.urlresolvers import reverse, NoReverseMatch
from django.forms.util import flatatt
from django.forms.widgets import Select
from django.utils.safestring import mark_safe

class StateDistrictAdminSelect(Select):

	def render(self, name, value, attrs=None, choices=(),app_label=None,model=None):
		admin_url = reverse('admin:propertys_district_ajax_view') 
		if value is None: value = ''
		final_attrs = self.build_attrs(attrs, name=name)
		output=[u'<select%s>' % flatatt(final_attrs)]
		options = self.render_options(choices, [value])
		if options:
			output.append(options)
		output.append(u'</select>')
		output.append(u'''
		<script type="text/javascript">
			django.jQuery(document).ready(function($) {
				$("select#id_state").change(function(){
					var state=$(this).attr('value');
					$.ajax({
						type:"POST",
						// TODO: change to url django variable
						url:'%s',
						data: {'state':state},
						timeout: 5000,
						dataType:"json",
						error: function(error){
							alert('Error District LOAD: entre em contato com administrador');
						},
						success: function(retorno) {
							var select_id = false;
							$("select#id_district_fk option").each(function(){
									if ($(this).val() !== ''){
										if ( $(this).attr('selected') ) 
											select_id=$(this).val();
										$(this).remove();
									}
							});	
							$.each(retorno, function(i, item) {
								if (item.pk == select_id) 
									$('select#id_district_fk').append('<option selected="selected" value="'+item.pk+'">'+item.fields.district+'</option>');
								else
									$('select#id_district_fk').append('<option value="'+item.pk+'">'+item.fields.district+'</option>');
							});
						},
					});
				}).change();
			});
		</script>
		''' % (admin_url)
		)
		return mark_safe(u'\n'.join(output))