"use strict";
var chartTextColor = '#96A2B4';

if ($("#message-list").length) {
	$("#message-list").css({
		height : 400
	}).niceScroll();
}

/* chart shadow */
var draw = Chart.controllers.line.prototype.draw;
Chart.controllers.lineShadow = Chart.controllers.line.extend({
	draw : function() {
		draw.apply(this, arguments);
		var ctx = this.chart.chart.ctx;
		var _stroke = ctx.stroke;
		ctx.stroke = function() {
			ctx.save();
			ctx.shadowColor = '#00000075';
			ctx.shadowBlur = 10;
			ctx.shadowOffsetX = 8;
			ctx.shadowOffsetY = 8;
			_stroke.apply(this, arguments)
			ctx.restore();
		}
	}
});

function monthlySalesChart() {
	var options = {
		series: [{
		name: 'Sales Goal',
		type: 'column',
		data: [210, 315, 299, 415, 456, 413, 399, 352, 452, 320, 257,333]
	  }, {
		name: 'Achieved Sales',
		type: 'line',
		data: [250, 300, 289, 475, 488, 489, 388, 312, 472, 300, 297,333]
	  }],
		chart: {
		height: 350,
		type: 'line',
		toolbar : {
			show : false,
		}
	  },
	  colors: ['#cdb4cf','#9234eb'],
	  stroke: {
		width: [0, 4]
	  },
	  
	  dataLabels: {
		enabled: true,
		enabledOnSeries: [1],
		style: {
			colors: ['#968a96','#9234eb']
		}
		
	  },
	  labels: ['Jan', 'Feb', 'Mar', 'Apr','May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
	  
	  
	  };

	var chart = new ApexCharts(document.querySelector("#monthlySalesChart"), options);

	chart.render();

}

monthlySalesChart();

function yearlySalesChart() {
	var options = {
		series : [ {
			name : 'Revenue',
			data : [ 87, 57, 74, 88, 75, 45, 69 ],
			labels : [ "thousands" ]
		}, {
			name : "Expense",
			data : [ 35, 41, 62, 42, 13, 18, 29 ],
			labels : [ "thousands" ]
		}, {
			name : 'Profit',
			data : [ 60, 47, 68, 74, 70, 36, 60 ],
			labels : [ "thousands" ]
		} ],
		xaxis : {
			categories : [ "2020", "2019", "2018", "2017", "2016", "2015","2014" ]
		},
		chart : {
			type : 'line',
			height : 350,
			toolbar : {
				show : false
			},
			dropShadow: {
				enabled: true,
				enabledOnSeries: undefined,
				bottom: 10,
				left: 0,
				color: '#000',
				opacity: 0.35
			}
		},
		dataLabels : {
			enabled : false
		},
		stroke: {
			curve: 'smooth',
			width: [4, 4, 4],
          	dashArray: [0, 3, 3]
		},
		markers: {
			size: 0,
			hover: {
				size: 2,
				sizeOffset: 3
			}
		},
	};

	 
	var chart = new ApexCharts(document.querySelector("#yearlySalesChart"), options);

	chart.render();
}

yearlySalesChart();

function salesBySocialSourceChart() {
	var options = {
		series: [76, 67, 61, 90],
		chart: {
		height: 350,
		type: 'radialBar',
	  },
	  plotOptions: {
		radialBar: {
		  offsetY: 0,
		  startAngle: 0,
		  endAngle: 270,
		  hollow: {
			margin: 5,
			size: '30%',
			background: 'transparent',
			image: undefined,
		  },
		  dataLabels: {
			name: {
			  show: false,
			},
			value: {
			  show: false,
			}
		  }
		}
	  },
	  colors: ['#ee0979', '#16c655', '#39539E', '#0077B5'],
	  labels: ['Instagram', 'Whatsup', 'Facebook', 'LinkedIn'],
	  legend: {
		show: true,
		floating: true,
		fontSize: '10px',
		position: 'bottom',
		offsetX: 1,
		offsetY: 1,
		labels: {
		  useSeriesColors: true,
		},
		markers: {
		  size: 0
		},
		formatter: function(seriesName, opts) {
		  return seriesName + ":  " + opts.w.globals.series[opts.seriesIndex]
		},
		itemMargin: {
		  vertical: 3
		}
	  },
	  responsive: [{
		breakpoint: 480,
		options: {
		  legend: {
			  show: false
		  }
		}
	  }]
	  };

	  var chart = new ApexCharts(document.querySelector("#salesBySocialSourceChart"), options);
	  chart.render();
}

salesBySocialSourceChart();


function chart1(){
	
    var options = {
            series: [{
            name: 'Total Earning',
            data: [80, 60, 100, 80, 130, 100, 150]
		  }],
		  sparkline: {
			enabled: true
		  },
            chart: {
            height: 120,
            type: 'line',
            toolbar : {
				show : false
			}
          },
          colors:['#FFF'],
          dataLabels: {
            enabled: false
          },
          stroke: {
	          curve: 'smooth'
	        },
	        grid: {
	            show: false,
	            padding: {
	                top: -15,
	                right: 0,
	                bottom: 0,
	                left: 0
	            }
			},
			markers: {
				size: 0,
				hover: {
				  size: 2,
				  sizeOffset: 3
				}
			},
          xaxis: {
        	  show : false,
				position : 'bottom',
				labels : {
					offsetY : -1,
					show : false
				},
				axisBorder : {
					show : false
				},
				axisTicks : {
					show : false
				},
				tooltip : {
					enabled : false,
					

				}
          },
          yaxis: {
			  show : false,
			  min: 50,
			  max: 160
	        }
          };

	        var chart = new ApexCharts(document.querySelector("#chart-1"), options);
	        chart.render();
	
}
chart1();

function chart2(){
	
	var options = {
		series: [{
		name: 'Total Earning',
		data: [80, 60, 100, 80, 130, 100, 150]
	  }],
	  sparkline: {
		enabled: true
	  },
		chart: {
		height: 120,
		type: 'line',
		toolbar : {
			show : false
		}
	  },
	  colors:['#FFF'],
	  dataLabels: {
		enabled: false
	  },
	  stroke: {
		  curve: 'smooth'
		},
		grid: {
			show: false,
			padding: {
				top: -15,
				right: 0,
				bottom: 0,
				left: 0
			}
		},
		markers: {
			size: 0,
			hover: {
			  size: 2,
			  sizeOffset: 3
			}
		},
	  xaxis: {
		  show : false,
			position : 'bottom',
			labels : {
				offsetY : -1,
				show : false
			},
			axisBorder : {
				show : false
			},
			axisTicks : {
				show : false
			},
			tooltip : {
				enabled : false,
				

			}
	  },
	  yaxis: {
		  show : false,
		  min: 50,
		  max: 160
		}
	  };

	        var chart = new ApexCharts(document.querySelector("#chart-2"), options);
	        chart.render();
	
}
chart2();

function chart3(){
	
	var options = {
		series: [{
		name: 'Total Earning',
		data: [80, 60, 100, 80, 130, 100, 150]
	  }],
	  sparkline: {
		enabled: true
	  },
		chart: {
		height: 120,
		type: 'line',
		toolbar : {
			show : false
		}
	  },
	  colors:['#FFF'],
	  dataLabels: {
		enabled: false
	  },
	  stroke: {
		  curve: 'smooth'
		},
		grid: {
			show: false,
			padding: {
				top: -15,
				right: 0,
				bottom: 0,
				left: 0
			}
		},
		markers: {
			size: 0,
			hover: {
			  size: 2,
			  sizeOffset: 3
			}
		},
	  xaxis: {
		  show : false,
			position : 'bottom',
			labels : {
				offsetY : -1,
				show : false
			},
			axisBorder : {
				show : false
			},
			axisTicks : {
				show : false
			},
			tooltip : {
				enabled : false,
				

			}
	  },
	  yaxis: {
		  show : false,
		  min: 50,
		  max: 160
		}
	  };


	        var chart = new ApexCharts(document.querySelector("#chart-3"), options);
	        chart.render();
	
}
chart3();


function chart4(){
	
	var options = {
		series: [{
		name: 'Total Earning',
		data: [80, 60, 100, 80, 130, 100, 150]
	  }],
	  sparkline: {
		enabled: true
	  },
		chart: {
		height: 120,
		type: 'line',
		toolbar : {
			show : false
		}
	  },
	  colors:['#FFF'],
	  dataLabels: {
		enabled: false
	  },
	  stroke: {
		  curve: 'smooth'
		},
		grid: {
			show: false,
			padding: {
				top: -15,
				right: 0,
				bottom: 0,
				left: 0
			}
		},
		markers: {
			size: 0,
			hover: {
			  size: 2,
			  sizeOffset: 3
			}
		},
	  xaxis: {
		  show : false,
			position : 'bottom',
			labels : {
				offsetY : -1,
				show : false
			},
			axisBorder : {
				show : false
			},
			axisTicks : {
				show : false
			},
			tooltip : {
				enabled : false,
				

			}
	  },
	  yaxis: {
		  show : false,
		  min: 50,
		  max: 160
		}
	  };


	        var chart = new ApexCharts(document.querySelector("#chart-4"), options);
	        chart.render();
	
}
chart4();