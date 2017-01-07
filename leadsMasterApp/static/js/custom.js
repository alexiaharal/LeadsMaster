
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

    var monthsArray = new Array();
    monthsArray["January"] = "0";
    monthsArray["February"] = "1";
    monthsArray["March"] = "2";
    monthsArray["April"] = "3";
    monthsArray["May"] = "4";
    monthsArray["June"] = "5";
    monthsArray["July"] = "6";
    monthsArray["August"] = "7";
    monthsArray["September"] = "8";
    monthsArray["October"] = "9";
    monthsArray["November"] = "10";
    monthsArray["December"] = "11";

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

$(document).ready(function(){
    calendarHome()
})

function calendarHome(){
    var d = new Date();
    mainFunction(d);
}

function nextFunction() {
    var month =((document).getElementById('currMonth')).innerHTML;
    var year = ((document).getElementById('currYear')).innerHTML;
    var current = new Date(year,monthsArray[month],1);
    var next= new Date(current.setMonth( current.getMonth( ) + 1 ));
    mainFunction(next)
}

function prevFunction() {
    var month =((document).getElementById('currMonth')).innerHTML;
    var year = ((document).getElementById('currYear')).innerHTML;
    var current = new Date(year,monthsArray[month],1);
    var previous= new Date(current.setMonth( current.getMonth( ) - 1 ));
    mainFunction(previous)
}
function mainFunction(d){
    $('.days').empty()
    html=""

    //save month as a number and as a word to be displayed
    var month=d.getMonth()
    namedmonth=months[d.getMonth()];
    var year=d.getFullYear();

    //display month name
    document.getElementById("currMonth").innerHTML=namedmonth;
    document.getElementById("currYear").innerHTML=year;

    //find out what day is the first and last day of the month
        // in order to get days of the previous/upcoming month

    var FirstDay = new Date(year, month, 1);
    var LastDay = new Date(year, month + 1, 0);

    if (typeof weekday[FirstDay.getDay()] != 'undefined') {     // CHECK FOR 'undefined'.
        FirstDay=FirstDay
        LastDay= LastDay
    }
    else {
        FirstDay=""
        LastDay=""
    }

    //get number of days this month
    days= LastDay.getDate();

    //get previous/upcoming month's number of days
    var futureMonth= new Date(d.setMonth( d.getMonth( ) + 1 ));
    var pastMonth = new Date(d.setUTCMonth(month - 1));
    var LastPastDay = new Date(pastMonth.getFullYear(), pastMonth.getMonth()+1, 0).getDay();
    var LastMonthDays= new Date(pastMonth.getFullYear(), pastMonth.getMonth()+1, 0).getDate();
    var FirstFutureDay = new Date(futureMonth.getFullYear(),futureMonth.getMonth(),1).getDay();

    if (FirstDay.getDay()==0){
        for (var i=LastMonthDays-5; i <= LastMonthDays; i++) {
          href="<a href=\"{% url 'calendarDay' day="+i+" month="+(pastMonth.getMonth()+1)+" year="+pastMonth.getFullYear()+" %}\">"
          html +=href+ "<li>"+(i)+"</li></a>";
        }
    }else{
        for (var i=LastMonthDays-FirstDay.getDay()+2; i <= LastMonthDays; i++) {
          href="<a href=\"{% url 'calendarDay' day="+i+" month="+pastMonth.getMonth()+1+" year="+pastMonth.getFullYear()+" %}\">"
          html +=href+"<li>"+(i)+"</li></a>";
        }
    }
    for (var i=0; i < days; i++) {
      href="<a href=\"{% url 'calendarDay' day="+(i+1)+" month="+month+" year=" +year" %}\">"
      html +="<li><b>"+(i+1)+"</b></li></a>";
    }
    for (var i=1; i <= 7-LastDay.getDay(); i++) {
      href="<a href=\"{% url \'calendarDay' day="+i+" month="+futureMonth.getMonth()+" year="+futureMonth.getFullYear()+" %}\">"
      html +="<li>"+(i)+"</li></a>";
    }


    $("#daysBuilder").append(html);
    };
// Get the modal
var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}