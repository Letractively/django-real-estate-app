(function($) {
	$(document).ready(function() {
		$("select#id_state").change(function(){
				var state=$(this).attr('value');
				$.ajax({
					type:"POST",
					url:'/admin/propretys/district/ajax/',
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
	})
 })(django.jQuery)
