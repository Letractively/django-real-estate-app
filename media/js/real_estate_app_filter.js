(function($){
	$(document).ready(function(){
		$('#changelist').removeClass('filtered');
		$('#changelist-filter').attr('rel','hidden');
		$('#changelist-filter > h2').addClass('down');

		$('#changelist-filter > h2').click(function(){
			if ($('#changelist-filter').attr('rel') === 'hidden') {
				$('#changelist').addClass('filtered');
				$('#changelist-filter-content').show();
				$('#changelist-filter').attr('rel','show');
				$('#changelist-filter > h2').removeClass('down');
				$('#changelist-filter > h2').addClass('up');
			 } else {
				$('#changelist').removeClass('filtered');
				$('#changelist-filter-content').hide();
				$('#changelist-filter').attr('rel','hidden');
				$('#changelist-filter > h2').removeClass('up');
				$('#changelist-filter > h2').addClass('down');
			}
		});
	})
})(django.jQuery);