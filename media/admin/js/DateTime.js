(function($){
	$(document).ready(function(){
		$('div#time-widget').each(function() {
			$(this).datetimepicker({
      			pickDate: false
    		})
		});
    	$('div#date-widget').each(function() {
			$(this).datetimepicker({
      			pickTime: false
      		});
    	});
	})
})(jQuery);