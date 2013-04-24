(function($) {
	$(document).ready(function($){
		$('#id_cpf').autocompleteselectmutiple({
			'source':'/imoveis/calendar/visitor/search/',
			'fields':['visitor_first_name',]
		})
	});
})(django.jQuery)