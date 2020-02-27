var stickyHeaders = (function() {
	var $window = $(window), $stickies;
	var load = function(stickies) {
		if (typeof stickies === "object" && stickies instanceof jQuery && stickies.length > 0) {
			$stickies = stickies.each(function() {
				var $thisSticky = $(this).wrap('<div class="followWrap" />');
				$thisSticky.data('originalPosition', $thisSticky.offset().top).data('originalHeight', $thisSticky.outerHeight()).parent().height($thisSticky.outerHeight()); 			  
			});
			$window.off("scroll.stickies").on("scroll.stickies", function() {
				_whenScrolling();		
			});
		}
	};

	var _whenScrolling = function() {
		$stickies.each(function(i) {			
			var $thisSticky = $(this), $stickyPosition = $thisSticky.data('originalPosition');
			if ($stickyPosition <= $window.scrollTop()) {        
				var $nextSticky = $stickies.eq(i + 1), $nextStickyPosition = $nextSticky.data('originalPosition') - $thisSticky.data('originalHeight');
				$thisSticky.addClass("fixed");
				if ($nextSticky.length > 0 && $thisSticky.offset().top >= $nextStickyPosition) {
					$thisSticky.addClass("absolute").css("top", $nextStickyPosition);
				}
			} else {
				var $prevSticky = $stickies.eq(i - 1);
				$thisSticky.removeClass("fixed");
				if ($prevSticky.length > 0 && $window.scrollTop() <= $thisSticky.data('originalPosition') - $thisSticky.data('originalHeight')) {
					$prevSticky.removeClass("absolute").removeAttr("style");
				}
			}
		});
	};

	return {
		load: load
	};
})();

// Cache selectors
var 	lastId,
topMenu = $("#horizon-sticky-nav"),
topMenuHeight = topMenu.outerHeight()+90,
// All list items
menuItems = topMenu.find("a"),
// Anchors corresponding to menu items
scrollItems = menuItems.map(function(){
	var item = $($(this).attr("href"));
	if (item.length) { return item; }
});

// Bind click handler to menu items
// so we can get a fancy scroll animation
menuItems.on("click",function(e){
	var 	href = $(this).attr("href"),
		offsetTop = href === "#" ? 0 : $(href).offset().top-120;
		// offsetTop = href === "#" ? 0 : $(href).offset().top-topMenuHeight+1;
	$('html, body').stop().animate({ 
		scrollTop: offsetTop
	}, 300);
	e.preventDefault();
});

// Bind to scroll
$(window).scroll(function(){
	// Get container scroll position
	var fromTop = $(this).scrollTop()+topMenuHeight;
 
	// Get id of current scroll item
	var cur = scrollItems.map(function(){
		if ($(this).offset().top < fromTop)
		 return this;
	});
	// Get the id of the current element
	cur = cur[cur.length-1];
	var id = cur && cur.length ? cur[0].id : "";
 
	if (lastId !== id) {
		 lastId = id;
		 // Set/remove active class
		 menuItems.parent().removeClass("active").end().filter("[href='#"+id+"']").parent().addClass("active");
	}                   
});

$(function() {
	stickyHeaders.load($(".fullwidth-horizon-sticky"));
});