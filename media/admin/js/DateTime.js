(function($){
	$(document).ready(function(){
		$('.inline-actived div#time-widget').datetimepicker({
      			pickDate: false
    	});
    	$('.inline-actived div#date-widget').datetimepicker({
      			pickTime: false
      	});
	})
})(jQuery);