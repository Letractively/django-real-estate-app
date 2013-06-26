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

				var setResize = function(container){
					var width = container.width() || options.width;
					var height = container.height() || options.height;

					options.height=height
					options.width=width

					if (height < 200)
						options.height=height*3

				}
				
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
					 marker:{
					 	options:{draggable:true},
					 	latLng:default_position(),
					 	events: {
					 		dragend: function(marker) {
	 							var position = marker.getPosition();
				 				$(options.point_y).attr('value',position.lat());
						 		$(options.point_y).attr('value',position.lng());
							},
					 	},
					},
					height:300,
					width:300,
				});

				return this.each( function() {
					setResize($(this));
				 	$(this).width(options.width).height(options.height).gmap3(options);
				});
		};
	
})(django.jQuery)
