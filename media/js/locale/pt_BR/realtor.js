(function($) {

	function hiden_pj_fields() {
		$('#id_realtor_set-0-cnpj').parent().hide();
		$('#id_realtor_set-0-razao_social').parent().hide();
		$('#id_realtor_set-0-responsavel').parent().hide();
	}

	function hiden_pf_fields() {
		$('#id_realtor_set-0-sex').parent().hide();
		$('#id_realtor_set-0-rg').parent().hide();
		$('#id_realtor_set-0-cpf').parent().hide();
		$('#id_realtor_set-0-ssp').parent().hide();
	}

	function show_pf_fields() {
		$('#id_realtor_set-0-sex').parent().show();
		$('#id_realtor_set-0-rg').parent().show();
		$('#id_realtor_set-0-cpf').parent().show();
		$('#id_realtor_set-0-ssp').parent().show();
	}

	function show_pj_fields() {
		$('#id_realtor_set-0-cnpj').parent().show();
		$('#id_realtor_set-0-razao_social').parent().show();
		$('#id_realtor_set-0-responsavel').parent().show();
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