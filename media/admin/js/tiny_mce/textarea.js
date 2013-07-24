(function($) {
   $(document).ready(function () {
        var width= $('.real_content > .span7').width()-130;
        var height = $('.real_content > .span7').height()/4;

        var toolbar = "undo redo | styleselect formatselect fontselect fontsizeselect | forecolor backcolor | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | bullist numlist | outdent indent | table image media | link unlink anchor"
        var toolbar320 = "bold italic underline strikethrough | alignleft aligncenter alignright alignjustify"

        var plugins = [ "advlist autolink lists link image charmap print preview hr anchor pagebreak", "visualblocks visualchars code fullscreen", "media nonbreaking table contextmenu directionality", "template paste textcolor"]
        var plugins320 = [ "pagebreak",]
        
        toolbar   = width <= 320 ? toolbar320 : toolbar
        plugins   = width <= 320 ? plugins320 : plugins
        statusbar = width <= 320 ? false : true

        tinymce.init({
            selector: "textarea",
            plugins: plugins ,
            menubar: false,
            toolbar: toolbar,
            statusbar:statusbar

        });

    });
})(django.jQuery);
