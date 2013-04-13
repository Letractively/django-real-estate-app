(function(a){
	a.fn.createTabs=function(){
		var b=a(this);
		b.find(".tab-content").hide();
		var d = b.find("ul.tabs li.active")
		d.show();
		var content=d.find("a").attr("href");
		b.find(content).show();
		b.find("ul.tabs li").click(function(){
			b.find("ul.tabs li").removeClass("active");
			a(this).addClass("active");
			b.find(".tab-content").hide();
			var c=a(this).find("a").attr("href");
			a(c).fadeIn();
			if (a(this).text() === "MAPS") {
				initgmaps();
			}
			return false 
		})
	}
})(django.jQuery);
