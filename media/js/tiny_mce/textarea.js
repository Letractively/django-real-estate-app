   tinyMCE.init({
        // General options
        mode : "textareas",
        theme : "advanced",
        plugins : "pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,wordcount,advlist,autosave",

        // Theme options
    
theme_advanced_buttons1 : "fullscreen,|,preview,|,cut,copy,paste,pasteword,|,undo,redo,|,search,replace,|,code,|,cleanup,|,bold,italic,underline,strikethrough,|,forecolor,backcolor,|,justifyleft,justifycenter,justifyright,justifyfull,|,help",
        theme_advanced_buttons2 : "removeformat,styleselect,formatselect,fontselect,fontsizeselect,|,bullist,numlist,outdent,indent,|,link,unlink,anchor",         
        theme_advanced_buttons3 : "sub,sup,|,image,insertdate,inserttime,|,tablecontrols,|,hr,advhr,visualaid,|,charmap,emotions,iespell,flash,|,print",
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "left",
        theme_advanced_statusbar_location : "bottom",
		width: "790",
		height: "590",
        // Example content CSS (should be your site CSS)
        content_css : "css/content.css",

        // Drop lists for link/image/media/template dialogs
        template_external_list_url : "lists/template_list.js",
        external_link_list_url : "lists/link_list.js",
        external_image_list_url : "lists/image_list.js",
        media_external_list_url : "lists/media_list.js",

        // Style formats
    }); 

