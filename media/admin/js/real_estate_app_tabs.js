(function ($,dj) {
	$(document).ready(function ($) {
	    $('#myTab a').click(function (e) {
	    	e.preventDefault();
	    	$(this).tab('show');
	    	if ($(this).attr('href') === "#maps") {
	    		dj('#gmaps').realEstateAppGmap({
	    			point_x:"#id_gmap_point_x",
	    			point_y:"#id_gmap_point_y",
	    		});
	    	}
	    });
	    $('#myTab a:first').tab('show');
	});
})(jQuery,django.jQuery)