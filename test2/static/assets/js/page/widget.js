
function myChart(){
	
	var options = {
	    	series: [{
	          name: 'Total Revenue',
	          data: [69, 45, 61, 43, 54, 37]
	        },{
				name: 'Total Profit',
				data: [55, 31, 47, 31, 43, 26]
			  }],
	          chart: {
	          height: 300,
	          type: 'line',
	          toolbar : {
					show : false
				}
	        },
	        colors:['#E91E63','#69e7b8'],
	        stroke: {
	          curve: 'smooth'
	        },
	        labels: ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
	        
	        tooltip: {
	          shared: true,
	          intersect: false,
	          y: {
	            formatter: function (y) {
	              if(typeof y !== "undefined") {
	                return  y.toFixed(0) + " points";
	              }
	              return y;
	            }
	          }
	        }
	        };
	
	        var chart = new ApexCharts(document.querySelector("#myChart"), options);
	        chart.render();
}
myChart();

function myChart2(){
var ctx = document.getElementById("myChart2").getContext('2d');
var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    datasets: [{
      label: 'Statistics',
      data: [525, 447, 326, 452, 560, 510, 620, 526, 620, 423, 590, 650],
      borderWidth: 2,
      backgroundColor: '#befad1',
      borderColor: 'transparent',
      borderWidth: 2.5,
      pointBackgroundColor: '#ffffff',
      pointRadius: 4
    }, {
      label: 'Statistics',
      data: [422, 410, 380, 516, 600, 355, 490, 560, 630, 420, 600, 440],
      borderWidth: 2,
      backgroundColor: '#34eb89',
      borderColor: 'transparent',
      borderWidth: 0,
      pointBackgroundColor: '#999',
      pointRadius: 4
    }]
  },
  options: {
    legend: {
      display: false
    },
    scales: {
      yAxes: [{
        gridLines: {
          drawBorder: false,
          color: '#f2f2f2',
        },
        ticks: {
          beginAtZero: true,
          stepSize: 150,
          fontColor: "#9aa0ac", // Font Color
        }
      }],
      xAxes: [{
        gridLines: {
          display: false
        },
        ticks: {
          fontColor: "#9aa0ac", // Font Color
        }
      }]
    },
  }
});
}
myChart2();


function referral(){
	
	function generateData(baseval, count, yrange) {
	    var i = 0;
	    var series = [];
	    while (i < count) {
	      //var x =Math.floor(Math.random() * (750 - 1 + 1)) + 1;;
	      var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
	      var z = Math.floor(Math.random() * (75 - 15 + 1)) + 15;
	  
	      series.push([baseval, y, z]);
	      baseval += 86400000;
	      i++;
	    }
	    return series;
	  }
	var options = {
	          series: [{
	          name: 'Chrome',
	          data: generateData(new Date('20 April 2020 GMT').getTime(), 20, {
	            min: 10,
	            max: 70
	          })
	        },
	        {
	          name: 'Firefox',
	          data: generateData(new Date('20 April 2020 GMT').getTime(), 20, {
	            min: 10,
	            max: 50
	          })
	        },
	        {
	          name: 'Safari',
	          data: generateData(new Date('20 April 2020 GMT').getTime(), 10, {
	            min: 30,
	            max: 50
	          })
	        },
	        {
	          name: 'Opera',
	          data: generateData(new Date('20 April 2020 GMT').getTime(), 10, {
	            min: 10,
	            max: 40,
	          })
	        }],
	          chart: {
	          height: 325,
	          type: 'bubble',
	          toolbar : {
					show : false
				}
	        },
	        colors:['#fa55e1', '#a0fa7a', '#fa9c55', '#55b2fa'],
	        dataLabels: {
	          enabled: false
	        },
	        fill: {
	          type: 'gradient',
	        },
	        xaxis: {
	          tickAmount: 12,
	          type: 'datetime',
	          labels: {
	              rotate: 0,
	          }
	        },
	        yaxis: {
	          max: 70
	        },
	        theme: {
	          palette: 'palette2'
	        },
	        legend : {
				 position: 'top'
			}
	        };

	        var chart = new ApexCharts(document.querySelector("#referral"), options);
	        chart.render();
	
}
referral();


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
            type: 'area',
            toolbar : {
				show : false
			}
          },
          colors:['#2e9de4'],
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
	                bottom: -10,
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
		type: 'area',
		toolbar : {
			show : false
		}
	  },
	  colors:['#ffc200'],
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
				bottom:-10,
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
		type: 'area',
		toolbar : {
			show : false
		}
	  },
	  colors:['#ee0979'],
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
				bottom: -10,
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
		type: 'area',
		toolbar : {
			show : false
		}
	  },
	  colors:['#69e7b8'],
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
				bottom: -10,
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

function visitorChart(){
	
	var options = {
		series: [{
		data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
	  }],
		chart: {
		type: 'bar',
		height: 340,
		toolbar : {
			show : false
		}
	  },
	  plotOptions: {
		bar: {
		  horizontal: true,
		  distributed: true,
		}
	  },
	  dataLabels: {
		enabled: false
	  },
	  xaxis: {
		categories: ['South Korea', 'Canada', 'United Kingdom', 'Franch', 'Italy', 'India', 'Japan',
		  'United States', 'China', 'Germany'
		],
	  }
	  };

	  var chart = new ApexCharts(document.querySelector("#visitorChart"), options);
	  chart.render();
	
}
visitorChart();
