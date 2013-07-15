(function($){
	$(document).ready(function(){
		$('div#time-widget').datetimepicker({
      			pickDate: false
    	});
    	$('div#date-widget').datetimepicker({
      			pickTime: false
      	});
	})
})(jQuery);