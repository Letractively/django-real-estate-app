(function($){
	$(document).ready(function(){
		$('#changelist').removeClass('filtered');
		$('#changelist-filter').attr('rel','hidden');
		$('#changelist-filter > h2').addClass('down');

		$('#changelist-filter > h2.down').click(function(){
				$('#changelist').addClass('filtered');
				$('#changelist-filter-content').show();
				$('#changelist-filter').attr('rel','show');
				$('#changelist-filter > h2').removeClass('down');
				$('#changelist-filter > h2').addClass('up');
		});
		// $('#changelist-filter > h2').click(function(){
		// 	if ($(this).attr('class') === 'up') {
		// 		$('#changelist').removeClass('filtered');
		// 		$('#changelist-filter-content').hide();
		// 		$('#changelist-filter').attr('rel','hidden');
		// 		$('#changelist-filter > h2').removeClass('up');
		// 		$('#changelist-filter > h2').addClass('down');
		// 	}
		// });
		// Problem with down and up...
	})
})(django.jQuery);