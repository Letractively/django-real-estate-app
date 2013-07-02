/*=============================================================
 * This plugin needed bootstrap-datetimepicker and google chart.
 *
 ==============================================================
 *
 *
 =============================================================*/
google.load('visualization',  '1', {'packages':['corechart']});
(function($){
	$.fn.realcharts= function(options) {		
		defaults ={
			'dataTable':[],
			'ajaxUrl':'',
			'display':'',
			'gchart': {
				'pointSize': 5,
				'title': "{{ title_chart }}",
			},
			'select_chart':[
				['custom','Custom <div id="dates"><div class="input-append" id="date_init_datetimepicker"> <input data-format="yyyy-MM-dd" type="text" id="date_init" value="" /> <span class="add-on"><i data-time-icon="icon-time" data-date-icon="icon-calendar"></i></span> </div> - <div class="input-append" id="date_end_datetimepicker"><input data-format="yyyy-MM-dd" id="date_end" type="text" value="" /><span class="add-on"><i data-time-icon="icon-time" data-date-icon="icon-calendar"></i></span></div></div>'],
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
			var dataTable = tableDataRequest({display:settigns.display});
			var chart, gdata, goptions = null;

			function init(){				
				chart=drawChart(dataTable,settigns.type_chart);
				if (settigns.type_chart != 'PieChart') 
					initSelectChart();
				
				$('#'+select_id).bind('changeValueChartOnSelect',function(event,dataTable){
					chart=drawChart(dataTable,settigns.type_chart);
				})

			}

			function tableDataRequest(params) {
				var results = settigns.dataTable;
				if (settigns.ajaxUrl) {
					$.ajax({
				          url: settigns.ajaxUrl,
				          dataType:"json",
				          async: false,
				          data:params,
				          success:function(data,jqXHR){
				          		results = data;
				          }
				    });
			    }
			    return results;

			}

			function initSelectChart() {
				var options=settigns.select_chart;
				html='<div class="dropdown" id="'+select_id+'">'
				html+= '<div class="btn dropdown-toggle" data-toggle="dropdown"> Selecione <span class="caret"></span></div>'
				html+='<ul class="dropdown-menu" id="chart-items">'
				for (option in options){
					html+='<li value="'+options[option][0]+'"><span>'+options[option][1]+'</span></li>'
				}
				html+='<li class="divider" ></li><li value="none"><span > <span class="btn btn-primary"> Filtrar </span></span></li>'
				html+='</ul></div>';
				$(containerId).before(html);

				// When containerId gets ready call connect events and others.
				$(containerId).ready(function(){
					$('#date_init_datetimepicker, #date_end_datetimepicker')
					.datetimepicker({
      							pickTime: false
    				});

					//hide custom date.
    				$('#'+select_id+' #dates').hide();
    			
					$('#'+select_id+' ul.dropdown-menu li').on('click',function(e){
					 	e.preventDefault();
					 	params ={}
					 	
						if( $(this).attr('selected') != 'selected' && $(this).attr('value')!='none') {
							//Clean selected object and set seleceted
							$(this).parent().find('li[selected]')
							.removeAttr('selected').find('span.icon-ok').detach();

							$(this).children().first().prepend('<span class="icon-ok"></span> ')
							$(this).attr('selected','selected');
							//alert($(this).attr('value'))
							$('#'+select_id+' #dates').hide();
							if ($(this).attr('value') === 'custom' ) $('#dates').show(); 
						}

						if ($(this).attr('value') === 'none'){
							// Get selected object
							selected = $(this).parent().find('li[selected]')
							params=$.extend(params,{'type':selected.attr('value')})
							
							if (selected.attr('value') === 'custom' ) {
								var date_init=selected.find('#date_init').val();
								var date_end=selected.find('#date_end').val();
								params=$.extend(params,{
									'date_init':date_init,
									'date_end':date_end
							    });
							} 

							//Get data from url and refresh graph with new data.
							dataTable=tableDataRequest(params);
							$(this).trigger('changeValueChartOnSelect',dataTable);
							$('#'+select_id).removeClass('open');
							
							return true;
						}

						return false;
					});
				});

			}

			function pointClicked(){
	  			var selection = chart.getChart().getSelection();
	  			if (selection[0].row != null){
	  				var date=gdata.getValue(selection[0].row,0);
	  				var date_end=date.split(' ')[0]+' 23:59:59'
	  				var tdate = new Date();
	  				
	  				if (date.split(' ')[1] != '00:00:00' || tdate.getHours() === 0 ) {
	  					hour=date.split(' ')[1];
	  					date_end=date.split(' ')[0]+' '+hour.split(':')[0]+':59:59';
	  				}
	  				params={
	  					type:'clicks',
	  					date_init:date,
	  					date_end:date_end
	  				}
	  				dateData=tableDataRequest(params)
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
				if (chart_type != 'PieChart')
			    	google.visualization.events.addListener(wrapper, 'select', pointClicked);
			    
			    wrapper.draw()
			    return wrapper
			}

			init();
			
		});
				
	}
})(jQuery);