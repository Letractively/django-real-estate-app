/* ============================================================
 * django-real-estate-app
 * http://code.google.com/p/django-real-estate-app
 * ============================================================
 * Copyright 2013 
 * This code is based on bootstrap-fileupload.js j2
 * http://jasny.github.com/bootstrap/javascript.html#fileupload
 *  
 * ============================================================
 * IMPORTANT: This custom works with bootstrap-tooltip.js
 * ========================================================= */
(function($){
  $(document).on('click.fileupload.data-api', '[data-provides="fileupload"]', function (e) {
    var $this = $(this);
    $this.find(':file').on('change.fileupload',function(e){
    	file = e.target.files !== undefined ? e.target.files[0] : (e.target.value ? { name: e.target.value.replace(/^.+\\/, '') } : null);
	  	if ( $(this).attr('data-target') && file ) {
			var reader = new FileReader();
			var target=$(this).attr('data-target');

	  	var preview=$(document).find('ul.thumbnails').find('li[data-target="'+target+'"]').find('.thumbnail');
			var element = this.$element;

			reader.onload = function(e) {
				var caption = preview.find('img').attr('data-original-title') === true ? '' : 'data-original-title="'+preview.find('img').attr('data-original-title')+'" title="" '
        var datatoggle = preview.find('img').attr('data-toggle') === true ? '' : 'data-toggle="'+preview.find('img').attr('data-toggle')+'" '
        var dataplacement = preview.find('img').attr('data-placement') === true ? '' : 'data-placement="'+preview.find('img').attr('data-placement')+'" '
				preview.html('<img '+caption+datatoggle+dataplacement+' src="' + e.target.result + '" ' + (preview.css('max-height') != 'none' ? 'style="max-height: ' + preview.css('max-height') + ';"' : '') + ' />');
			}
			reader.readAsDataURL(file);
	  	}  		
  	});
    if ($this.data('fileupload')) return
    $this.fileupload($this.data());
    var $target = $(e.target).closest('[data-dismiss="fileupload"],[data-trigger="fileupload"]');
    if ($target.length > 0) {
      $target.trigger('click.fileupload')
      e.preventDefault()
    }
  })
})(window.jQuery);