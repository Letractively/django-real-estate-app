(function($) {
   $(document).ready(function () {
        var width= $('.real_content > .span7').width()-130;
        var height = $('.real_content > .span7').height()/4;
        tinymce.init({
            selector: "textarea",
            plugins: [
                "advlist autolink lists link image charmap print preview hr anchor pagebreak",
                "visualblocks visualchars code fullscreen",
                "media nonbreaking table contextmenu directionality",
                "template paste textcolor"
            ],
            menubar: false,
            toolbar: "undo redo | styleselect formatselect fontselect fontsizeselect | forecolor backcolor | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | bullist numlist | outdent indent | table image media | link unlink anchor",

        });

    });
})(django.jQuery);
