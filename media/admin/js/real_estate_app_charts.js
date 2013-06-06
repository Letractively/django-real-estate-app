google.load('visualization',  '1', {'packages':['corechart']});
(function($){
	$.fn.realcharts= function(options) {		
		defaults ={
			'dataTable':[],
			'ajaxUrl':'',
			'gchart': {
				'pointSize': 5,
				'title': "{{ title_chart }}",
			},
			'select_chart':[
				['custom','Custom'],
				['week','Week'],
				['today','Today'],
				['month','Month'],
				['year','Year']
			]
		}

		var settigns=$.extend(defaults,options);
		
		return this.each(function() {
			var $this=$(this);
			var html_id = $(this).attr('id');
			var select_id = html_id+'-select';
			var containerId=document.getElementById(html_id);
			var dataTable = tableDataRequest();
			var chart, gdata, goptions = null;

			function init(){				
				chart=drawChart(dataTable,settigns.type_chart);
				initSelectChart();
				$('#'+select_id).bind('changeValueChartOnSelect',function(event,dataTable){
					chart=drawChart(dataTable,settigns.type_chart);
				})
			}

			function tableDataRequest(url) {
				var results = settigns.dataTable;
				if (settigns.ajaxUrl) {
					if (! url )
						url=settigns.ajaxUrl;
					$.ajax({
				          url: url,
				          dataType:"json",
				          async: false,
				          success:function(data,jqXHR){
				          		results = data;
				          }
				    });
			    }
			    return results;

			}

			function initSelectChart() {
				var options=settigns.select_chart;
				html = '<select id="'+select_id+'">'
				for (option in options){
					html+='<option value="'+options[option][0]+'">'+options[option][1]+'</option>'
				}
				html+='</select>';
				$(containerId).before(html);
				$('#'+select_id).change(function(){
					dataTable=tableDataRequest(settigns.ajaxUrl+'?display='+$(this).val());
					$(this).trigger('changeValueChartOnSelect',dataTable);
				})

			}

			function pointClicked(){

	  			var selection = chart.getChart().getSelection();
	  			if (selection[0].row != null){
	  				var date=gdata.getValue(selection[0].row,0).split(' ')[0];
	  				dateData=tableDataRequest(settigns.ajaxUrl+'?display=clicks&date_init='+date+'&date_end='+date)
	  				drawChart(dateData,'Table')
	  			}	
			}

			function drawChart(data,chart_type,extra_options={}){

				gdata = new google.visualization.DataTable(data);
			    goptions = $.extend(extra_options,settigns.gchart);

				wrapper = new google.visualization.ChartWrapper({
					chartType: chart_type,
					dataTable: gdata,
					options: goptions,
					containerId: containerId,
				});

			    google.visualization.events.addListener(wrapper, 'select', pointClicked);
			    
			    wrapper.draw()
			    return wrapper
			}

			init();
			
		});
				
	}
})(jQuery);