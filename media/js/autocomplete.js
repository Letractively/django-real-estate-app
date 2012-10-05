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
	 				objects.push("Clique para dicionar");
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
				if (!pk) {

					$('a#'+id)
					.facebox({'id':id,
					          'ajax_url':options.ajax_url_facebox})
					.trigger('click.facebox');
				}
				else {
					if (prev.indexOf("|"+pk+"|") == -1) {
						$this.val((prev ? prev : "|") + pk + "|");
						addItem(ui.item, pk)
						$text.val('');
					}
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
				});
			}

			$text.autocomplete({
				source: sourceRealEstate,//options.source,
				select: selectRealEstate,
				change: changeRealEstate,
				focus: itemFocus
			})

			$(".remove", document.getElementById("custom-"+id)).live("click", function(){  
		    	$(this).parent().remove();  
		    	removeItem($(this).attr('value'));
	           	if($("#custom-"+id+" span").length === 0) {  
		       		$text.css("top", 0);  
	       		}                 
	    	});  	
			
	    });
	}

})(django.jQuery)