(function($) {

	function hiden_pj_fields() {
		$('.cnpj').hide();
		$('.razao_social').hide();
		$('.responsavel').hide();
		$('.tipo_pessoa').hide();
	}

	function hiden_pf_fields() {
		$('.sex').hide();
		$('.rg').hide();
		$('.cpf').hide();
		$('.ssp').hide();
		$('.tipo_pessoa').hide();
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
    	$.fn.createTabs=function(){
    		var a=$;
			var b=a(this);
			b.find(".tab-content").hide();
			var d = b.find("ul.tabs li.active")
			d.show();
			var content=d.find("a").attr("href");
			b.find(content).show();
			b.find("ul.tabs li").click(function(){
				b.find("ul.tabs li").removeClass("active");
				a(this).addClass("active");
				b.find(".tab-content").hide();
				var c=a(this).find("a").attr("href");
				a(c).fadeIn();
				if (c=="#pessoa_juridica") {
					hiden_pf_fields();
    				show_pj_fields();
				} 
				if (c== "#pessoa_fisica") {
					hiden_pj_fields();
					show_pf_fields();
				}

				return false 
			})
		}
		
    	$('.inline-related').createTabs();

    	hiden_pj_fields();

    	
    });
})(django.jQuery);