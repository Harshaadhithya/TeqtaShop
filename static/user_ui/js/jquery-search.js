console.log("hey buddy!!");



(function($) {
	
	$.fn.jqSearch = function( options ) {
	
		var elems = this;
	
		var opt = $.extend({
			searchInput			: '#search',
			searchTarget		: 'data',
			searchData			: 'search-data',
			animation			: 'fade', // fade, slide
		}, options);
		
		$(opt.searchInput).on('keyup', function() {
			
			var searchString = $(opt.searchInput).val();
			
			
			elems.each(function() {
			
				var searchText = $(this).attr('data-'+opt.searchData);
				elem = $(this);
				
				if (opt.searchTarget == 'text') {
					searchText = elem.text();
				} else if (opt.searchTarget == 'data') {
					searchText = elem.attr('data-'+opt.searchData);
				} else {
					searchText = elem.attr('data-'+opt.searchData);
				}

				
				var regex = new RegExp( '(' + searchString + ')', 'gi' );
				if ( ! regex.test( searchText ) ) {
					elem.addClass('wfHide');
				} else {
					elem.addClass('wfShow');
					console.log( searchText );
				}
				
			});
			if (opt.animation == 'fade') {
				$('.wfHide').fadeOut().removeClass('wfHide');
				$('.wfShow').fadeIn().removeClass('wfShow');
			} else if (opt.animation == 'slide') {
				$('.wfHide').slideUp().removeClass('wfHide');
				$('.wfShow').slideDown().removeClass('wfShow');
			}
		});
	}
	
})(jQuery);
