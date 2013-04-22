(function($){
    $(document).ready(function($) {
		$.mask.masks = django.jQuery.extend(django.jQuery.mask.masks,{
			'money': { mask: '99,999.999.999.999', type: 'reverse',defaultValue: '000'},
			'zip_code': { mask: '99999-999'},
			'decimal': {mask:'99.999999999999',type:'reverse'},
			'area': {mask:'99,999.999.999.999',type:'reverse',defaultValue: '000'},
			'phone':{mask:'+99 (999) 99999-9999'},
		});

		$('input:text').setMask();

		$('#proprety_form').submit(function() {
			django.jQuery('input:text').each(function (){
				if (django.jQuery(this).attr('alt')==='money' || django.jQuery(this).attr('alt') === 'area') {
					var val =django.jQuery(this).val();
					django.jQuery(this).val($.mask.string(val,'decimal'));
				}
			})
		});

		$('td[alt="price"]').each( function () {
			$(this).html('R$ '+$.mask.string($(this).text(),'money'));
		});

	});
})(django.jQuery);
