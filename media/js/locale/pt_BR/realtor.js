(function($) {

	function hiden_pj_fields() {
		$('.cnpj').hide();
		$('.razao_social').hide();	
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
	}

	function simulate_required_fields(){
		$('.rg > div > label').attr('class','required');
		$('.cpf > div > label').attr('class','required');
		$('.ssp > div > label').attr('class','required');
		$('.cnpj > div > label').attr('class','required');
		$('.razao_social > div > label').attr('class','required');
	}

    $(document).ready(function($) {
    	$('.tipo_pessoa > div > select').change(function(e){
    		var value=$(this).val();
    		if (value=="PJ"){
    			hiden_pf_fields();
    			show_pj_fields();
    		} else if (value=="PF") {
    			hiden_pj_fields();
    			show_pf_fields();
    		}
    	})
    	$('.tipo_pessoa > div > select > option').each(function(){
    		value=$(this).attr('selected') ? $(this).val() : false
    		if (value == "PJ")
    			hiden_pf_fields()
    		else if (value == "PF")
    			hiden_pj_fields()
    	})
    	
    	simulate_required_fields();

    });

})(django.jQuery);