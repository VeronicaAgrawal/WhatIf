// --SEARCH BUTTON DASHBOARD--//
//$(document).ready(function(){
//    $("#seachbtn").click(function(){
//		$("#showsearchresult").show();
//	});
//});

//-- DASHBOARD PIE CHART --//
$(function (){
   
   $(document).ready(function () {

       var isBig = $(window).width() == 768;
       
       var legendBig = {
           align: 'right',
           verticalAlign: 'middle',
           layout: 'vertical'
       };
       
       var legendSmall = {
           align: 'center',
           verticalAlign: 'bottom',
           layout: 'vertical'
       };
       
       // Build the chart
   });
});
function pieHCH() {
       $('#container').highcharts({
           chart: {
               plotBackgroundColor: null,
               plotBorderWidth: null,
               plotShadow: false,
               type: 'pie'
           },
           title: {
               text: ''
           },
           tooltip: {
               pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
           },
//           legend: isBig? legendBig : legendSmall,
           plotOptions: {
               pie: {
                   allowPointSelect: true,
                   cursor: 'pointer',
                   dataLabels: {
                       enabled: false
                   },
                   showInLegend: true
               }
           },
           series: [{
               name: 'Brands',
               colorByPoint: true,
               data: [{
                   name: 'Price Index Low',
                   y: 105,
                   color:'#a6f685',
               }, {
                   name: 'Price Index Mid',
                   y: 220,
                   color:'#f4b908',

               }, {
                   name: 'Price Index High',
                   y: 550,
                   color:'#f99192',
               },]
           }]
       });
}
//-- DASHBOARD TABLE POP UP--//
$(function(){

<!-- var appendthis =  ("<div class='modal-overlay js-modal-close'></div>"); -->
	$('td[data-modal-id]').mouseover(function(e) {	
    $(".modal-overlay").fadeTo(500, 0.7);   
		var popBox = $(this).attr('data-modal-id');
		$('#'+popBox).fadeIn($(this).data());
	});  
  
  
$('td[data-modal-id]').mouseout(function() {
    $(".popbox, .modal-overlay").fadeOut(500, function() {
        $(".modal-overlay").remove();
    });
 
});
 
$(window).resize(function() {
    $(".popbox").css({
        top: ($(window).height() - $(".popbox").outerHeight()) / 2,
        left: ($(window).width() - $(".popbox").outerWidth()) / 2
    });
});
 
$(window).resize();
 
});


// -- Optimized Page Line Graph --//

//function lineHCH() {
//    $('#container1').highcharts({
//        title: {
//            text: '',
//
//        },
//        subtitle: {
//            text: '',
//            x: -20
//        },
//        xAxis: {
//            title: {
//                text: 'week no.'
//            },
//
//            categories: ['1', '6', '11', '16', '21', '26',
//                '31', '36', '41', '46', '51', '56']
//        },
//        yAxis: {
//            title: {
//                text: 'Sales'
//            },
//            plotLines: [{
//                value: 0,
//                width: 1,
//                color: '#808080'
//            }]
//        },
//        tooltip: {
//            valueSuffix: ''
//        },
//        legend: {
//            layout: 'vertical',
//            align: 'right',
//            verticalAlign: 'middle',
//            borderWidth: 0,
//            x: 0,
//            y: -100,
//            lineSpacing:20,
//        },
//        series: [{
//            name: 'Current Price',
//            data: [ 5.1, 6.9, 4.5, 15.2, 7.5, 3.2, 2.5, 3.3, 4.3, 3.9, 6.6]
//        }, {
//            name: 'Optimized Price',
//            data: [0.5, 10.1, 30.8, 10.1, 11.5, 5.29, 20.8, 4.1]
//        },
//        ]
//    });
//}

/*-- Negative 0 Positive Rane --*/
var rangeSlider = function(){  
    var slider = $('.range-slider'),      
      range = $('.range-slider__range'),     
       value = $('.range-slider__value');       

        slider.each(function(){   
           value.each(function(){    
               var value = $(this).prev().attr('value');   
                 $(this).html(value);                  
             });  
                   range.on('input', function(){    
                     $(this).next(value).html(this.value);  

                 });  
               });
    };rangeSlider();

   /*-- Optimized Scale Slider-- */

//   pieHCH();
//   lineHCH();

