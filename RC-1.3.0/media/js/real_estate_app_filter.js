(function($){
	$(document).ready(function(){
		$('#changelist-filter > h2').addClass('up');

		$('#changelist-filter > h2#filter').click(function(event){
				if ($(this).attr('class') === 'up') {
					$('#changelist-filter > h2').removeClass('up')
					$('#changelist-filter > h2').addClass('down')
					if ($('div#changelist').hasClass('filtered'))
						$('#changelist').removeClass('filtered');
				} else {
					$('#changelist-filter > h2').removeClass('down')
					$('#changelist-filter > h2').addClass('up')
					if (!$('div#changelist').hasClass('filtered'))
						$('#changelist').addClass('filtered');
				}
				
				$('#changelist-filter-content').slideToggle();
		});
});
})(django.jQuery);