function initgmaps() {
			var $ = django.jQuery;

			var map, marker;
			var zoom = 11;
			var lat_x = $('input#id_gmap_point_x').val();  
			var lat_y = $('input#id_gmap_point_y').val();
	
			if (lat_x != '-15.793905' && lat_y != '-47.882395')
				var zoom = 18;
	
			map = new google.maps.Map($('#gmaps').get(0), {
			        zoom: zoom,
					center: new google.maps.LatLng(lat_x, lat_y),
			        mapTypeId: google.maps.MapTypeId.ROADMAP
			});
		
			center = new google.maps.LatLng( lat_x , lat_y);
			marker = new google.maps.Marker({map: map, position: center, draggable: true});
			google.maps.event.addListener(map,'rightclick',function(event) {
				marker.setPosition(event.latLng);
				map.setCenter(event.latLng)
				var position = marker.getPosition();
				$("input#id_gmap_point_x").val(position.lat());
				$("input#id_gmap_point_y").val(position.lng());
			});
			google.maps.event.addListener(marker,'dragend',function() {
				var position = marker.getPosition();
				$("input#id_gmap_point_x").val(position.lat());
				$("input#id_gmap_point_y").val(position.lng());
			});
}
