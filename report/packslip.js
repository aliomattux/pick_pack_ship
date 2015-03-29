function bailworkingfooter() {
var bodyHeight = $("page").height();
var pageHeight = 1800;
var pushHeight = pageHeight - bodyHeight;
var p = $('<div style="height:', pushHeight, ';"></div>');
if (pageHeight > bodyHeight) {
    $(".footer").prepend(p)
}
}
function bunkworkingfooter() {
var bodyHeight = $("page").height();
var pageHeight = 1800;
var pushHeight = pageHeight - bodyHeight;
if (pageHeight > bodyHeight) {
    $(".push").css("height",pushHeight);
}
}
function pooworkingfooter() {
var bodyHeight = $("body").height();
var pageHeight = $("window").height();
if (pageHeight > bodyHeight) {
    $(".footer").css("position", "absolute").css("bottom",0);
}
}
function pushfooter(linecount) {
var pushHeight = ( 18 - parseInt(linecount) ) + 40;
$(".push:last").css("height", pushHeight);
}
function newpushfooter(linecount) {
var pushHeight = ( 20*(18 - parseInt(linecount)) ) + 1;
$(".push:last").css("height", pushHeight);
}
function jqfooter() {
$(window).bind("load", function() { 
       
       var footerHeight = 0,
           footerTop = 0,
           $footer = $("#footer");
           
       positionFooter();
       
       function positionFooter() {
       
                footerHeight = $footer.height();
                footerTop = ($(window).scrollTop()+$(window).height()-footerHeight)+"px";
       
               if ( ($(document.body).height()+footerHeight) < $(window).height()) {
                   $footer.css({
                        position: "absolute"
                   }).animate({
                        top: footerTop
                   })
               } else {
                   $footer.css({
                        position: "static"
                   })
               }
               
       }

       $(window)
               .scroll(positionFooter)
               .resize(positionFooter)
               
});
}
function setprinted() {
$(".onebytwo:last").addClass("onebytworeprinted");
}
function highlightme() {
$(".highlightme").each( function(i) {
if ( parseFloat($(this).html()) > parseFloat('1.00') ) {
$(this).addClass("bold");
}
});
}
function subst() {
var vars={};
var x=document.location.search.substring(1).split('&');
for(var i in x) {var z=x[i].split('=',2);vars[z[0]] = unescape(z[1]);}
var x=['frompage','topage','page','webpage','section','subsection','subsubsection'];
for(var i in x) {
var y = document.getElementsByClassName(x[i]);
for(var j=0; j<y.length; ++j) y[j].textContent = vars[x[i]];
    }
}
function pagebreak() {
    "use strict";
    var pixelsOfHeight = 0;

    $('.pagebreak').each(function () {
        var h = $(this).height();
    /*
    $(this).append(pixelsOfHeight + ", " + h);
        $(this).append("<div>FOOBAR</div>");
        $(this).css("page-break-after", "always");
        $(this).css("page-break-inside", "avoid");
        $(this).css("page-break-before", "always");
        $(this).append(pixelsOfHeight + ", " + h);
    */

    if(h + pixelsOfHeight > 1450){
        /* Number above indicated page height ~ 1100.
           Number below indicates header height ~ 120.
        */
        pixelsOfHeight = h - 250;
        $(this).append('</div><div class="break"></div><div class="table">');

    }
    else {
        pixelsOfHeight += h;
    }
   });
}
function cleandecimals() {
$(".qty").each( function(i) {
$(this).html($(this).html().replace('.00',''));
$(this).html($(this).html().replace('0.0','0'));
});
}
function stripmw() {
$(".mwsku").each( function(i) {
$(this).html($(this).html().replace('MW-',''));
});
}
function pagecount() {
$(".pdfkit_page_count").each( function(i) {
mycount = maxcount;
$(this).html($(this).html().replace('abc', mycount));
});
}
function substringer() {
$(".description").each( function(i) {
$(this).html($(this).html().substring(0,24));
});
}
function barcode() {
$(".internalid").each( function(i) {
$(this).barcode ($(this).html(), "code128", {posY:12,barHeight:10, fontSize:6 } )
});
}
function tr_num() {
$(".ordernumber").each( function(i) {
$(this).barcode ($(this).html(), "code128", {barHeight:20,fontSize:20} )
});
}
function controlno() {
$(".controlno").each( function(i) {
$(this).barcode ($(this).html(), "code128", {barWidth:3,posX:0,fontSize:50,showHRI:true,barHeight:100} )
});
}
function onebytwo() {
$(".onebytwo").each( function(i) {
$(this).barcode ($(this).html(), "code128", {barWidth:1,posX:0,showHRI:true,barHeight:55} )
});
}
function totebarcode() {
$(".totebarcode").each( function(i) {
$(this).barcode ($(this).html(), "code128", {barWidth:1,posX:0,showHRI:false,barHeight:25} )
});
}
function scaletofit() {
    $('.onebytwo').imgscale({ 
        parent : '.non-immediate-parent-container', 
        fade : 1000 
      });
};
function scalefont() {
    $('.humanreadable').textfill({ maxFontPixels: 100 });
}
function showheight() {
$(".height").each( function(i) {
$(this).html ($(this).html().replace('', $(document).height()));
});
}
function totedisplay2() {
$(".totes").each( function(i) {
    var totetable = 
    '<div style="display: table; border: dotted black 1px;">' + 
    '<div style="display: table-row">' +
        '<div style="display: table-cell">A</div>' +
        '<div style="display: table-cell">B</div>' +
    '</div>' + 
    '</div>';
$(this).html($(this).html().replace('abc',totetable));
});
}
/*
    $("totes").replaceWith('<div>FOOOOOOOOOO</div>');
    */
function fotedisplay() {
$(".totes").each( function(i) {
    var test = '<div>woeijfweoijweoiejwoweifjweoij</div>';
    var totetable = 
    '<div style="display: table; border: dotted black 1px;">' + 
    '<div style="display: table-row">' +
        '<div style="display: table-cell">${order["totes"][0]</div>' +
        '<div style="display: table-cell">${order["totes"][1]</div>' +
    '</div>' + 
    '</div>';
$(this).live( function() {
    var $this = $(this);
    $this.replaceWith('<div>FOO</div>');
});
//$(this).html($(this).html(replaceWith('<div>FOO</div>'));
});
}
/*
  textfill
 @name      jquery.textfill.js
 @author    Russ Painter
 @author    Yu-Jie Lin
 @version   0.4.0
 @date      2013-08-16
 @copyright (c) 2012-2013 Yu-Jie Lin
 @copyright (c) 2009 Russ Painter
 @license   MIT License
 @homepage  https://github.com/jquery-textfill/jquery-textfill
 @example   http://jquery-textfill.github.io/jquery-textfill/index.html
*/
(function(e){e.fn.textfill=function(q){function m(){a.debug&&("undefined"!=typeof console&&"undefined"!=typeof console.debug)&&console.debug.apply(console,arguments)}function r(){"undefined"!=typeof console&&"undefined"!=typeof console.warn&&console.warn.apply(console,arguments)}function n(a,b,d,h,f,k){function c(a,b){var c=" / ";a>b?c=" > ":a==b&&(c=" = ");return c}m(a+"font: "+b.css("font-size")+", H: "+b.height()+c(b.height(),d)+d+", W: "+b.width()+c(b.width(),h)+h+", minFontPixels: "+f+", maxFontPixels: "+
k)}function p(a,b,d,h,f,k,c,l){for(n(a+": ",b,f,k,c,l);c<l-1;){var e=Math.floor((c+l)/2);b.css("font-size",e);if(d.call(b)<=h){if(c=e,d.call(b)==h)break}else l=e;n(a+": ",b,f,k,c,l)}b.css("font-size",l);d.call(b)<=h&&(c=l,n(a+"* ",b,f,k,c,l));return c}var a=e.extend({debug:!1,maxFontPixels:40,minFontPixels:4,innerTag:"span",widthOnly:!1,success:null,callback:null,fail:null,complete:null,explicitWidth:null,explicitHeight:null},q);this.each(function(){var g=e(a.innerTag+":visible:first",this),b=a.explicitHeight||
e(this).height(),d=a.explicitWidth||e(this).width(),h=g.css("font-size");m("Opts: ",a);m("Vars: maxHeight: "+b+", maxWidth: "+d);var f=a.minFontPixels,k=0>=a.maxFontPixels?b:a.maxFontPixels,c=void 0;a.widthOnly||(c=p("H",g,e.fn.height,b,b,d,f,k));f=p("W",g,e.fn.width,d,b,d,f,k);a.widthOnly?g.css("font-size",f):g.css("font-size",Math.min(c,f));m("Final: "+g.css("font-size"));g.width()>d||g.height()>b&&!a.widthOnly?(g.css("font-size",h),a.fail&&a.fail(this)):a.success?a.success(this):a.callback&&(r("callback is deprecated, use success, instead"),
a.callback(this))});a.complete&&a.complete(this);return this}})(window.jQuery);
