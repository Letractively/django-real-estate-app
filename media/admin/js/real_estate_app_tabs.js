(function ($,dj) {
	$(document).ready(function ($) {
	    $('#myTab').find('li').each(function(ct){
	    	$(this).children(':first').click(function (e) {
		    	e.preventDefault();
		    	$(this).tab('show');
		    	if ($(this).attr('href') === "#maps") {
		    		
		    		dj('#gmaps').realEstateAppGmap({
		    			point_x:"#id_gmap_point_x",
		    			point_y:"#id_gmap_point_y",
		    		});
		    	}
	    	});
	    	if ($(this).hasClass('errors') && ! $(this).parent().children().hasClass('active') ){
	    		$(this).find('a').tab('show');
	    	} else if (ct == 0 && ! $(this).parent().children().hasClass('errors') ) {
	    		$(this).find('a').tab('show');
	    	}
		});
	});
})(jQuery,django.jQuery)