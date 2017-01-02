
(function ($) {
    "use strict";
    var mainApp = {

        main_fun: function () {
            /*====================================
            METIS MENU 
            ======================================
            $('#main-menu').metisMenu();*/

            /*====================================
              LOAD APPROPRIATE MENU BAR
           ======================================*/
            $(window).bind("load resize", function () {
                if ($(this).width() < 768) {
                    $('div.sidebar-collapse').addClass('collapse')
                } else {
                    $('div.sidebar-collapse').removeClass('collapse')
                }
            });
       },

        initialization: function () {
            mainApp.main_fun();

        }

    }

});
//calendar functions
$(document).ready(function(){
    var html=""
    var months = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"];
    var weekday = new Array();
    weekday[0] = "Sunday";
    weekday[1] = "Monday";
    weekday[2] = "Tuesday";
    weekday[3] = "Wednesday";
    weekday[4] = "Thursday";
    weekday[5] = "Friday";
    weekday[6] = "Saturday";

    //get current date
    var d = new Date();
    //save month as a number and as a word to be displayed
    var month=d.getMonth()
    namedmonth=months[d.getMonth()];
    var year=d.getFullYear();

    //display month name
    document.getElementById("month").innerHTML=namedmonth;

    //find out what day is the first and last day of the month
        // in order to get days of the previous/upcoming month
    console.log('month: '+ namedmonth+ " " +month)

    var FirstDay = new Date(year, month, 1);
    var LastDay = new Date(year, month + 1, 0);

    if (typeof weekday[FirstDay.getDay()] != 'undefined') {     // CHECK FOR 'undefined'.
//        FirstDay=FirstDay.toDateString('dd/mon/yyyy')
//        LastDay= LastDay.toDateString('dd/mon/yyyy')
        FirstDay=FirstDay
        LastDay= LastDay
    }
    else {
        FirstDay=""
        LastDay=""
    }
    console.log('firstdaymonth: '+ FirstDay.toDateString('dd/mon/yyyy')+ " " +FirstDay.getDay())
    console.log('lastdaymonth: '+ LastDay.toDateString('dd/mon/yyyy')+ " " +LastDay.getDay())
    //get number of days this month
    days= LastDay.getDate();

    //get previous month's number of days
        var futureMonth = new Date(d.setUTCMonth(month + 1));

    var pastMonth = (new Date(d.setUTCMonth(month - 1)));
    var LastPastDay = new Date(pastMonth.getFullYear(), pastMonth.getMonth()+1, 0).getDay();
    var LastMonthDays= new Date(pastMonth.getFullYear(), pastMonth.getMonth()+1, 0).getDate();
    var FirstFutureDay = new Date(futureMonth.getFullYear(),futureMonth.getMonth(),1).getDay();
    console.log(LastPastDay)
    console.log(LastMonthDays)
    console.log(FirstFutureDay)

//    var prevMonthLastDay=new Date(d.getFullYear(), prevMonth, 0).getDay();
//    console.log(prevMonthLastDay)
    if (FirstDay.getDay()==0){
        for (var i=LastMonthDays-5; i <= LastMonthDays; i++) {
          html +="<li>"+(i)+"</li>";
        }
    }else{
        for (var i=LastMonthDays-FirstDay.getDay()-1; i <= LastMonthDays; i++) {
          html +="<li>"+(i)+"</li>";
        }
    }
    for (var i=0; i < days; i++) {
      html +="<li>"+(i+1)+"</li>";
    }
    $("#daysBuilder").append(html);
    });