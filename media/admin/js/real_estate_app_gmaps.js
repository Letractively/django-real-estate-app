/*
	This is a extend pluggins for jquery.gmap3: 
	http://gmap3.net


*/
(function($) {

		$.fn.realEstateAppGmap=function(options) {
				var point_x = $(options.point_x).val() || 0;
				var point_y = $(options.point_y).val() || 0;
				
				var default_position =function() {
					return [point_x,point_y];
				};

				var customDragend = function(marker) {
	 				var position = marker.getPosition();
	 				$(options.point_y).attr('value',position.lat());
			 		$(options.point_y).attr('value',position.lng());
				};
				
				options = $.extend(true, options, {
					 map:{
					    options:{
					    	center:default_position(),
					     	zoom:12,
					    },
					    events: {
					    	rightclick: function(event) {
					    		alert('fazer menu');
					    	}
					    }
					 },
					 marker: {
					 	options:{draggable:true},
					 	latLng:default_position(),
					 	events: {
					 		dragend: function(marker) {
	 							var position = marker.getPosition();
				 				$(options.point_y).attr('value',position.lat());
						 		$(options.point_y).attr('value',position.lng());
							},
					 	},
					}
				});
				return this.each( function() {
				 	$(this).gmap3(options);
				});
		};
	
})(django.jQuery)
