"use strict";
var chartTextColor = '#96A2B4';

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

function monthlyEarningChart() {
	var options = {
	          series: [{
	          name: 'Earning',
	          data: [30, 50, 70, 90, 110, 120, 120, 110, 90, 70, 50, 30]
	        }],
	          chart: {
	          height: 350,
	          type: 'bar',
	          toolbar : {
					show : false
				}
	        },
	        dataLabels: {
	          enabled: false
	        },
	        stroke: {
	          curve: 'straight'
			},
			plotOptions: {
				bar: {
					columnWidth: '45%',
					distributed: true,
					endingShape: 'rounded'
				}
			},
			colors:['#fc8d9f', '#fc8d9f','#fc8d9f', '#fc8d9f','#fc8d9f', '#fc8d9f','#ffd633','#ffd633','#ffd633','#ffd633','#ffd633','#ffd633'],
			xaxis: {
	          type: 'line',
	          categories: ["Jan", "Feb", "Mar", "Apr", "May", "June", "July","Aug","Sep","Oct","Nov","Dec"]
	        },
	        legend : {
				 position: 'top'
			}
	        };

	        var chart = new ApexCharts(document.querySelector("#monthlyEarningChart"), options);
	        chart.render();
}
monthlyEarningChart();

function yearlyRevenueChart() {

	var options = {
		series : [ {
			name : 'Revenue',
			data : [ 101, 99, 87, 145, 90, 78, 90 ],
			labels : [ "thousands" ]
		}, {
			name : "Expense",
			data : [ 59, 29, 25, 42, 13, 18, 29 ],
			labels : [ "thousands" ]
		}, {
			name : 'Profit',
			data : [ 42, 70, 62, 103, 77, 60, 61 ],
			labels : [ "thousands" ]
		} ],
		xaxis : {
			categories : [ "2020", "2019", "2018", "2017", "2016", "2015","2014" ]
		},
		chart : {
			type : 'area',
			height : 350,
			toolbar : {
				show : false
			}
		},
		dataLabels : {
			enabled : false
		},
		markers : {
			hover : {
				sizeOffset : 4
			}
		},
		legend : {
			 position: 'top'
		}
	};

	var chart = new ApexCharts(document.querySelector("#yearlyRevenueChart"),options);
	chart.render();
	
}
yearlyRevenueChart();

function openTicketsChart() {
	var options = {
		series: [78],
		chart: {
		height: 310,
		type: 'radialBar',
		offsetY: -10
	  },
	  plotOptions: {
		radialBar: {
		  startAngle: -140,
		  endAngle: 140,
		  dataLabels: {
			name: {
			  fontSize: '16px',
			  color: undefined,
			  offsetY: 120
			},
			value: {
			  offsetY: 76,
			  fontSize: '22px',
			  color: undefined,
			  formatter: function (val) {
				return val + "%";
			  }
			}
		  }
		}
	  },
	  fill: {
		type: 'gradient',
		gradient: {
			shade: 'dark',
			shadeIntensity: 0.15,
			inverseColors: false,
			opacityFrom: 1,
			opacityTo: 1,
			stops: [0, 50, 65, 91]
		},
	  },
	  stroke: {
		dashArray: 4
	  },
	  labels: ['Open Tickets'],
	  };

	  var chart = new ApexCharts(document.querySelector("#openTicketsChart"), options);
	  chart.render();
}
openTicketsChart();


function chart1(){
	
    var options = {
            series: [{
            name: 'Total Earning',
            data: [100, 60, 80, 70, 110, 90, 130,100,115,85,100, 130,100,145,125,150,140]
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
		  tooltip: {
			enabled: true,
			custom: function({series, seriesIndex, dataPointIndex, w}) {
				return   series[seriesIndex][dataPointIndex];
			},
		  },
          colors:['#FFF'],
          dataLabels: {
            enabled: false
          },
          stroke: {
			curve: 'straight',
			width: 3,
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
		data: [100, 60, 80, 70, 110, 90, 130,100,115,85,100, 130,100,145,125,150,140]
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
	  tooltip: {
		enabled: true,
		custom: function({series, seriesIndex, dataPointIndex, w}) {
			return   series[seriesIndex][dataPointIndex];
		},
	  },
	  colors:['#FFF'],
	  dataLabels: {
		enabled: false
	  },
	  stroke: {
		curve: 'straight',
		width: 3,
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
		data: [100, 60, 80, 70, 110, 90, 130,100,115,85,100, 130,100,145,125,150,140]
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
	  tooltip: {
		enabled: true,
		custom: function({series, seriesIndex, dataPointIndex, w}) {
			return   series[seriesIndex][dataPointIndex];
		},
	  },
	  colors:['#FFF'],
	  dataLabels: {
		enabled: false
	  },
	  stroke: {
		curve: 'straight',
		width: 3,
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
		data: [100, 60, 80, 70, 110, 90, 130,100,115,85,100, 130,100,145,125,150,140]
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
	  tooltip: {
		enabled: true,
		custom: function({series, seriesIndex, dataPointIndex, w}) {
			return   series[seriesIndex][dataPointIndex];
		},
	  },
	  colors:['#FFF'],
	  dataLabels: {
		enabled: false
	  },
	  stroke: {
		curve: 'straight',
		width: 3,
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