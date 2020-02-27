jQuery(function($) {



	"use strict";


	
	var $window = $(window);
	
	
	
	/**
	 * Main Menu Slide Down Effect
	 */
	 
	var mainNavbar = $(".main-nav-menu");		
		
	// Main Menu 
	mainNavbar.find('li').on("mouseenter", function() {
		$(this).find('ul').first().stop(true, true).delay(250).slideDown(500, 'easeInOutQuad');
	});
	mainNavbar.find('li').on("mouseleave", function() {
		$(this).find('ul').first().stop(true, true).delay(200).slideUp(150, 'easeInOutQuad');
	});

	// Arrow for Menu has sub-menu
	$(".navbar-arrow ul li").has("ul").children("a").append("<span class='arrow-indicator'></span>");

	
	
	/**
	 * Sticky Header
	 */
	 
	$(".with-waypoint-sticky").waypoint(function() {
		$("#header-waypoint-sticky").toggleClass("header-waypoint-sticky");
		return false;
	}, { offset: "-20px" });




	/**
	 *	Dropdown effect
	 */
	 
	var dropdownSmooth02 = $(".dropdown.dropdown-smooth-02");	

	dropdownSmooth02.on('show.bs.dropdown', function(e){
		var $dropdownSmooth02Menu = $(this).find('.dropdown-menu');
		var orig_margin_top = parseInt($dropdownSmooth02Menu.css('margin-top'));
		$dropdownSmooth02Menu.css({'margin-top': (orig_margin_top + 10) + 'px', opacity: 0}).animate({'margin-top': orig_margin_top + 'px', opacity: 1}, 300, function(){
			$(this).css({'margin-top':''});
		});
	});
	dropdownSmooth02.on('hide.bs.dropdown', function(e){
		var $dropdownSmooth02Menu = $(this).find('.dropdown-menu');
		var orig_margin_top = parseInt($dropdownSmooth02Menu.css('margin-top'));
		$dropdownSmooth02Menu.css({'margin-top': orig_margin_top + 'px', opacity: 1, display: 'block'}).animate({'margin-top': (orig_margin_top + 10) + 'px', opacity: 0}, 300, function(){
			$(this).css({'margin-top':'', display:''});
		});
	});
	
	
	
	/**
	 * Dropdown hover
	 */
	 
	var hoverDropdown = $(".dropdown-hover");
	hoverDropdown.on('mouseenter', function() {
		$(this).find('.dropdown-menu').stop(true, true).delay(150).slideDown(500, 'easeInOutQuad');
	});
	hoverDropdown.on('mouseleave', function() {
		$(this).find('.dropdown-menu').stop(true, true).delay(150).slideUp(250, 'easeInOutQuad');
	});

	
	
	/**
	* Bootstarp Dropdown as Select with active state
	*/
	
	$('.dropdown-select').on( 'click', '.dropdown-menu li a', function() { 
		var asSelectOption = $(this).html();

		//Adds active class to selected item
		$(this).parents('.dropdown-menu').find('li').removeClass('active');
		$(this).parent('li').addClass('active');

		//Displays selected text on dropdown-toggle button
		$(this).parents('.dropdown-select').find('.dropdown-toggle').html(asSelectOption + ' <span class="caret"></span>');
	});


	
	/**
	 * Bootstrap Tooltip
	 */
	 
	$('[data-toggle="tooltip"]').tooltip()
	
	
	
	/**
	 *  Tab in dropdown
	 */
	 
	$('.tab-in-dropdown').on('click', '.nav a', function(){
	    $(this).closest('.dropdown').addClass('dontClose');
	})

	$('.dropdown-tab').on('hide.bs.dropdown', function(e) {
		if ( $(this).hasClass('dontClose') ){
				e.preventDefault();
		}
		$(this).removeClass('dontClose');
	});

	$('a.tab-external-link').on("click",function (e) {
		e.preventDefault();
		var tabPattern=/#.+/gi //use regex to get anchor(==selector)
		var tabContentID = e.target.toString().match(tabPattern)[0]; //get anchor   
		$('.external-link-navs a[href="'+tabContentID+'"]').tab('show') ;         
	});
	
	
	
	/**
	 *  Open specific tab in modal
	 */
	 
	$('a[data-toggle=modal][data-target]').on("click",function() {
	    var tabTargetInModal = $(this).attr('href');
	    $('a[data-toggle=tab][href=' + tabTargetInModal + ']').tab('show');
	})
	

	/**
	 * Chosen
	 */
	 
	$(".chosen-the-basic").chosen({disable_search_threshold: 10}); 
	$(".chosen-no-search").chosen({disable_search: true}); 
	
	
	
	/**
	 * Sticky sidebar
	 */
	 
	$(".sticky-kit").stick_in_parent({
		offset_top: 105,
	});
	
	
	
	/**
	 * Input Spinner
	 */
	 
	$(".touch-spin-03").TouchSpin({
		min: 0,
		max: 100,
		verticalbuttons: true,
		buttondown_class: "btn btn-white",
		buttonup_class: "btn btn-white"
	});
	
	
	
	/**
	 * Date Picker
	 */
	 
	$('.air-datepicker').datepicker({
		minDate: new Date(),
	})
	$('.air-datepicker-with-time').datepicker({
		minDate: new Date(),
	})
	
	var $airDatepickerRangeStartGeneral = $('#airDatepickerRange-general #dateStart-general'),
		$airDatepickerRangeEndGeneral = $('#airDatepickerRange-general #dateEnd-general');

	$airDatepickerRangeStartGeneral.datepicker({
		onSelect: function (fd, date) {
			$airDatepickerRangeEndGeneral.data('datepicker').update('minDate', date);
			$airDatepickerRangeEndGeneral.focus();
		},
		language : "en",
		minDate: new Date(),
	})

	$airDatepickerRangeEndGeneral.datepicker({
		onSelect: function (fd, date) {
			$airDatepickerRangeStartGeneral.data('datepicker').update('maxDate', date)
		},
		autoClose: true,
		language : "en",
	})
	
	var $airDatepickerRangeStartHotel = $('#airDatepickerRange-hotel #dateStart-hotel'),
		$airDatepickerRangeEndHotel = $('#airDatepickerRange-hotel #dateEnd-hotel');

	$airDatepickerRangeStartHotel.datepicker({
		onSelect: function (fd, date) {
			$airDatepickerRangeEndHotel.data('datepicker').update('minDate', date);
			$airDatepickerRangeEndHotel.focus();
		},
		language : "en",
		minDate: new Date(),
	})

	$airDatepickerRangeEndHotel.datepicker({
		onSelect: function (fd, date) {
			$airDatepickerRangeStartHotel.data('datepicker').update('maxDate', date)
		},
		autoClose: true,
		language : "en",
	})
	
	var $airDatepickerRangeStartFlight = $('#airDatepickerRange-flight #dateStart-flight'),
		$airDatepickerRangeEndFlight = $('#airDatepickerRange-flight #dateEnd-flight');

	$airDatepickerRangeStartFlight.datepicker({
		onSelect: function (fd, date) {
			$airDatepickerRangeEndFlight.data('datepicker').update('minDate', date);
			$airDatepickerRangeEndFlight.focus();
		},
		language : "en",
		minDate: new Date(),
	})

	$airDatepickerRangeEndFlight.datepicker({
		onSelect: function (fd, date) {
			$airDatepickerRangeStartFlight.data('datepicker').update('maxDate', date)
		},
		autoClose: true,
		language : "en",
	})
	
	var $airDatepickerRangeStartGuide = $('#airDatepickerRange-guide #dateStart-guide'),
		$airDatepickerRangeEndGuide = $('#airDatepickerRange-guide #dateEnd-guide');

	$airDatepickerRangeStartGuide.datepicker({
		onSelect: function (fd, date) {
			$airDatepickerRangeEndGuide.data('datepicker').update('minDate', date);
			$airDatepickerRangeEndGuide.focus();
		},
		language : "en",
		minDate: new Date(),
	})

	$airDatepickerRangeEndGuide.datepicker({
		onSelect: function (fd, date) {
			$airDatepickerRangeStartGuide.data('datepicker').update('maxDate', date)
		},
		autoClose: true,
		language : "en",
	})
	
	
	
	/**
	 * Slick carousel
	 */
	 
	$('.slick-hero-slider').slick({
		dots: true,
		infinite: true,
		speed: 500,
		slidesToShow: 1,
		slidesToScroll: 1,
		centerMode: true,
		infinite: true,
		centerPadding: '0',
		focusOnSelect: true,
		adaptiveHeight: true,
		autoplay: true,
		autoplaySpeed: 4500,
		pauseOnHover: true,
	});
	
	$('.slick-hero-slider-02').slick({

		dots: false,
		arrows: false,
		infinite: true,
		speed: 500,
		slidesToShow: 1,
		slidesToScroll: 1,
		centerMode: true,
		infinite: true,
		centerPadding: '0',
		focusOnSelect: true,
		adaptiveHeight: true,
		autoplay: true,
		autoplaySpeed: 4500,
		pauseOnHover: false,
	});
	
	$('#slick-testimonial-long-slideshow').slick({
		slidesToShow: 1,
		slidesToScroll: 1,
		speed: 500,
		arrows: false,
		fade: true,
		adaptiveHeight: true,
		asNavFor: '#slick-testimonial-long-nav'
	});
	
	$('#slick-testimonial-long-nav').slick({
		slidesToShow: 3,
		slidesToScroll: 1,
		speed: 500,
		asNavFor: '#slick-testimonial-long-slideshow',
		dots: false,
		arrows: false,
		centerMode: true,
		focusOnSelect: true,
		infinite: true,
		centerPadding: '0',
		responsive: [,
			{
				breakpoint: 767,
				settings: {
					slidesToShow: 2,
					arrows: false,
				}
			},
			{
				breakpoint: 575,
				settings: {
					slidesToShow: 1,
					arrows: false
				}
			}
		]
	});
	
	$('.slick-product-item').slick({
		infinite: false,
		slidesToShow: 3,
		slidesToScroll: 1,
		dots: true,
		responsive: [
			{
				breakpoint: 991,
				settings: {
					slidesToShow: 2,
					arrows: false,
				}
			},
			{
				breakpoint: 575,
				settings: {
					slidesToShow: 1,
					arrows: false,
				}
			}
		]
	});

	$('a[data-toggle="tab"]').on('shown.bs.tab', function() {	
		$($(this).attr('href')).find('.slick-product-item-in-tab').slick({
			infinite: false,
			slidesToShow: 3,
			slidesToScroll: 1,
			dots: true,
			responsive: [
				{
					breakpoint: 991,
					settings: {
						slidesToShow: 2,
						arrows: false,
					}
				},
				{
					breakpoint: 575,
					settings: {
						slidesToShow: 1,
						arrows: false,
					}
				}
			]
		})
	}).first().trigger('shown.bs.tab');
	
	$('a[data-toggle="tab"]').on('shown.bs.tab', function() {	
		$($(this).attr('href')).find('.slick-product-item-in-tab-col-4').slick({
			infinite: false,
			slidesToShow: 4,
			slidesToScroll: 1,
			dots: true,
			responsive: [
				{
					breakpoint: 991,
					settings: {
						slidesToShow: 2,
						arrows: false,
					}
				},
				{
					breakpoint: 575,
					settings: {
						slidesToShow: 1,
						arrows: false,
					}
				}
			]
		})
	}).first().trigger('shown.bs.tab');
	
	$('.slick-product-item-col-1').slick({
		infinite: false,
		slidesToShow: 1,
		slidesToScroll: 1,
		dots: true,
		adaptiveHeight: true,
	});
	
	$('.gallery-slideshow').slick({
		slidesToShow: 1,
		slidesToScroll: 1,
		speed: 500,
		arrows: true,
		fade: true,
		asNavFor: '.gallery-nav'
	});
	
	$('.gallery-nav').slick({
		slidesToShow: 7,
		slidesToScroll: 1,
		speed: 500,
		asNavFor: '.gallery-slideshow',
		dots: false,
		centerMode: true,
		focusOnSelect: true,
		infinite: true,
		responsive: [
			{
			breakpoint: 1199,
			settings: {
				slidesToShow: 7,
				}
			}, 
			{
			breakpoint: 991,
			settings: {
				slidesToShow: 5,
				}
			}, 
			{
			breakpoint: 767,
			settings: {
				slidesToShow: 5,
				}
			}, 
			{
			breakpoint: 480,
			settings: {
				slidesToShow: 3,
				}
			}
		]
	});
	
	
	
	/**
	 * Counter - Number animation
	 */
	 
	$(".counter").countimator();
	
	
	
	/**
	 * Range Slider
	 */
	 
	$("#price_range").ionRangeSlider({
		type: "double",
		grid: true,
		min: 0,
		max: 1000,
		from: 200,
		to: 800,
		prefix: "$"
	});
	
	$("#star_range").ionRangeSlider({
		type: "double",
		grid: false,
		from: 1,
		to: 2,
		values: [
			"<i class='dripicons-star'></i>", 
			"<i class='dripicons-star'></i> <i class='dripicons-star'></i>",
			"<i class='dripicons-star'></i> <i class='dripicons-star'></i> <i class='dripicons-star'></i>", 
			"<i class='dripicons-star'></i> <i class='dripicons-star'></i> <i class='dripicons-star'></i> <i class='dripicons-star'></i>",
			"<i class='dripicons-star'></i> <i class='dripicons-star'></i> <i class='dripicons-star'></i> <i class='dripicons-star'></i> <i class='dripicons-star'></i>" 
		]
	});
	
	
	moment.locale("en-GB");
	var $rangeTime = $(".ionRangeSlider-05");
	var rangeTimeStart = moment("00:00", "HH:mm");
	var rangeEnd = moment("23:59", "HH:mm");
	var rangeTimeFrom = moment("06:00", "HH:mm");
	var rangeTimeTo = moment("20:00", "HH:mm");

	$rangeTime.ionRangeSlider({
		type: "double",
		grid: true,
		min: rangeTimeStart.format("x"),
		max: rangeEnd.format("x"),
		from: rangeTimeFrom.format("x"),
		to: rangeTimeTo.format("x"),
		step: 1800000,                // 30 minutes in ms
		prettify: function (num) {
		return moment(num, 'x').format("h:mm A");
		}
	});
	
	
	
	/**
	 * Smooth scroll to anchor
	 */
	 
	$('a.anchor[href*=#]:not([href=#])').on("click",function () {
		if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
			var target = $(this.hash);
			target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
			if (target.length) {
				$('html,body').animate({
					scrollTop: (target.offset().top - 250) // 70px offset for navbar menu
				}, 300);
				return false;
			}
		}
	});
	
	

	/**
	* Background changes on focusing div by .addclass method
	*/
	
	$(".bg-change-focus-addclass").on("focusin", function() {
		$(this).addClass("focus");
	}).on("focusout", function() {
		$(this).removeClass("focus");
	});
	
	
	
	/**
	 * Contact for validator
	 */
	 
	var contactFormValidator = $("#contact-form");	
	
	contactFormValidator.validator();

    contactFormValidator.on('submit', function (e) {
        if (!e.isDefaultPrevented()) {
            var url = "contact.php";

            $.ajax({
                type: "POST",
                url: url,
                data: $(this).serialize(),
                success: function (data)
                {
                    var messageAlert = 'alert-' + data.type;
                    var messageText = data.message;

                    var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                    if (messageAlert && messageText) {
                        $('#contact-form').find('.contact-successful-messages').html(alertBox);
                        $('#contact-form')[0].reset();
                    }
                }
            });
            return false;
        }
    })
	
	
	
	/**
	 * Back To Top
	 */
	
	var backToTop = $("#back-to-top");
	
	$window.scroll(function () {
		if ($(this).scrollTop() > 50) {
			backToTop.fadeIn();
		} else {
			backToTop.fadeOut();
		}
	});
	
	// scroll body to 0px on click
	backToTop.on("click",function () {
		backToTop.tooltip('hide');
		$('body,html').animate({
			scrollTop: 0
		}, 800);
		return false;
	});
	
	backToTop.tooltip('show');



});

