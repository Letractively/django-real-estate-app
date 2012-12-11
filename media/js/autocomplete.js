/*
This code is based on app django-ajax-selects
*/
(function($) {
	$.fn.autocompleteselectmutiple = function(options) {
		return this.each(function(){
			var id = this.id;
			var $text=$("#"+id+"_text")
			var $this=$(this);
			var self=this;

			function removeItem(pk) {
				$this.val($this.val().replace("|" + pk + "|", "|"));
			}

			function sourceRealEstate(request, add) {
				$.get(options.source,request, function(data) {
	 				var objects=[]
	 				data=$.parseJSON(data)
	 				$.each(data,function(i,val){
	 					objects.push(val);
	 				});
	 				var add_link = '';
	 				//objects.push("Clique para dicionar");
	 				add(objects);
	 			});
			}

			function addItem(value, pk) {
	 			var span=$('<span>').html(value.value);
	 			var a=$("<a>").addClass("remove").attr({
	 				href:"javascript:",
	 				title:"Remove "+value.real_value,
	 				value:pk
	 			}).text("x").appendTo(span);
	 			span.insertBefore($text);
			}

			function selectRealEstate(event, ui) {
				pk=ui.item.pk;
				prev = $this.val();

				if (prev.indexOf("|"+pk+"|") == -1) {
						$this.val((prev ? prev : "|") + pk + "|");
						addItem(ui.item, pk)
						$text.val('');
				}

				return false
			}

			function changeRealEstate(){
				$text.val("").css("top",2);
			}

			function itemFocus(event, ui) {
				return false;
				
			}

			if (options.initial) {
				$.each(options.initial, function(i, its){
						addItem(its,its.pk);
						if (its.pk) {
							prev = $this.val();
						    $this.val((prev ? prev : "|") + its.pk + "|");
						}
				});
			}

			$text.autocomplete({
				source: sourceRealEstate,//options.source,
				select: selectRealEstate,
				change: changeRealEstate,
				focus: itemFocus
			}).data( "autocomplete" )._renderMenu = function( ul, items ) {
				var that = this;
            	$.each( items, function( index, item ) {
                	that._renderItem( ul, item );
            	});
            	$(ul).append("<li class='ui-menu-item last' id='add_anoter' role='menuitem' onclick='django.jQuery(\"#"+id+"_add_icon\").facebox().trigger(\"click.facebox\");'><a class='ui-corner-all' tabindex='-1'> Clique para adicionar </a></li>");	
		    };

			$(".remove", document.getElementById("custom-"+id)).live("click", function(){  
		    	$(this).parent().remove();  
		    	removeItem($(this).attr('value'));
	           	if($("#custom-"+id+" span").length === 0) {  
		       		$text.css("top", 0);  
	       		}                 
	    	});

	    	$("#add_anoter").live("click", function(){
				$("#"+id+"_add_icon").facebox().trigger('click.facebox');	
			})
			
	    });

	}
	
	

})(django.jQuery)