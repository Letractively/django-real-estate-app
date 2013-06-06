(function($){
	$(document).ready(function() {

	$(function() {
		var win = $(window);
		// Full body scroll
		var isResizing = false;
		win.bind('resize',function() {
			if (!isResizing) {
				isResizing = true;
				var container = $('#content');
				// Temporarily make the container tiny so it doesn't influence the
				// calculation of the size of the document
				container.css({
					'width': 1,
					'height': 1
				});
				// Now make it the size of the window...
				container.css({
					'width': win.width()+25,
					'height': win.height()
				});
				isResizing = false;
				container.jScrollPane({
										'showArrows': false, 
					  					horizontalGutter:5,
					  					verticalGutter:5
				});
			}
		}).trigger('resize');
		// Workaround for known Opera issue which breaks demo (see
		// http://jscrollpane.kelvinluck.com/known_issues.html#opera-scrollbar )
		$('body').css('overflow', 'hidden');
		// IE calculates the width incorrectly first time round (it
		// doesn't count the space used by the native scrollbar) so
		// we re-trigger if necessary.
		if ($('#full-page-container').width() != win.width()) {
		win.trigger('resize');
		}
	});

	$('.jspDrag').hide();
	$('.jspScrollable').mouseenter(function(){
			$('.jspDrag').stop(true, true).fadeIn('slow');
	});
	$('.jspScrollable').mouseleave(function(){
	$('.jspDrag').stop(true, true).fadeOut('slow');
}); 
	})
})(django.jQuery)