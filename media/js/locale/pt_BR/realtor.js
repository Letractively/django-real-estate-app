(function($) {

	function hiden_pj_fields() {
		$('.cnpj').hide();
		$('.razao_social').hide();
		$('.responsavel').hide();
	}

	function hiden_pf_fields() {
		$('.sex').hide();
		$('.rg').hide();
		$('.cpf').hide();
		$('.ssp').hide();
	}

	function show_pf_fields() {
		$('.sex').show();
		$('.rg').show();
		$('.cpf').show();
		$('.ssp').show();
	}

	function show_pj_fields() {
		$('.cnpj').show();
		$('.razao_social').show();
		$('.responsavel').show();
	}

    $(document).ready(function($) {
    	hiden_pj_fields();
    	$('#id_realtor_set-0-tipo_pessoa').change(function(event){
            var value=$('#id_realtor_set-0-tipo_pessoa :selected').val();
    		if (value == "PF") {
    			hiden_pj_fields();
    			show_pf_fields();
    		}
    		if (value == "PJ") {
    			hiden_pf_fields();
    			show_pj_fields();
    		}

    	});
    });
})(django.jQuery);