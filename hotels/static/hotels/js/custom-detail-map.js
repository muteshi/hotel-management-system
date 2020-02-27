function initialize() {

	// Create an array of styles.
	var styles = [{"featureType":"all","elementType":"labels","stylers":[{"lightness":63},{"hue":"#ff0000"}]},{"featureType":"administrative","elementType":"all","stylers":[{"hue":"#000bff"},{"visibility":"on"}]},{"featureType":"administrative","elementType":"geometry","stylers":[{"visibility":"on"}]},{"featureType":"administrative","elementType":"labels","stylers":[{"color":"#4a4a4a"},{"visibility":"on"}]},{"featureType":"administrative","elementType":"labels.text","stylers":[{"weight":"0.01"},{"color":"#727272"},{"visibility":"on"}]},{"featureType":"administrative.country","elementType":"labels","stylers":[{"color":"#ff0000"}]},{"featureType":"administrative.country","elementType":"labels.text","stylers":[{"color":"#ff0000"}]},{"featureType":"administrative.province","elementType":"geometry.fill","stylers":[{"visibility":"on"}]},{"featureType":"administrative.province","elementType":"labels.text","stylers":[{"color":"#545454"}]},{"featureType":"administrative.locality","elementType":"labels.text","stylers":[{"visibility":"on"},{"color":"#737373"}]},{"featureType":"administrative.neighborhood","elementType":"labels.text","stylers":[{"color":"#7c7c7c"},{"weight":"0.01"}]},{"featureType":"administrative.land_parcel","elementType":"labels.text","stylers":[{"color":"#404040"}]},{"featureType":"landscape","elementType":"all","stylers":[{"lightness":16},{"hue":"#ff001a"},{"saturation":-61}]},{"featureType":"poi","elementType":"labels.text","stylers":[{"color":"#828282"},{"weight":"0.01"}]},{"featureType":"poi.government","elementType":"labels.text","stylers":[{"color":"#4c4c4c"}]},{"featureType":"poi.park","elementType":"all","stylers":[{"hue":"#00ff91"}]},{"featureType":"poi.park","elementType":"labels.text","stylers":[{"color":"#7b7b7b"}]},{"featureType":"road","elementType":"all","stylers":[{"visibility":"on"}]},{"featureType":"road","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"labels.text","stylers":[{"color":"#999999"},{"visibility":"on"},{"weight":"0.01"}]},{"featureType":"road.highway","elementType":"all","stylers":[{"hue":"#ff0011"},{"lightness":53}]},{"featureType":"road.highway","elementType":"labels.text","stylers":[{"color":"#626262"}]},{"featureType":"transit","elementType":"labels.text","stylers":[{"color":"#676767"},{"weight":"0.01"}]},{"featureType":"water","elementType":"all","stylers":[{"hue":"#0055ff"}]}];

	var loc, map, marker, infobox;

	var styledMap = new google.maps.StyledMapType(styles,  {name: "Styled Map"});

	loc = new google.maps.LatLng($("#hotel-detail-map").attr("data-lat"), $("#hotel-detail-map").attr("data-lon"));

	map = new google.maps.Map(document.getElementById("hotel-detail-map"), {
		zoom: 14,
		center: loc,
		scrollwheel: false,
		//draggable:true,
		navigationControl: false,
		scaleControl: false,
		mapTypeControl:false,
		streetViewControl: false,
		mapTypeControlOptions: {
			mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style']
		},
		mapTypeId: google.maps.MapTypeId.ROADMAP,
	});

	//Associate the styled map with the MapTypeId and set it to display.
	map.mapTypes.set('map_style', styledMap);
	map.setMapTypeId('map_style');

	marker = new google.maps.Marker({
		map: map,
		position: loc,
		//disableDefaultUI:true,

		icon:'images/map-marker/00.png',
		//pixelOffset: new google.maps.Size(-140, -100),
		visible: true

		//animation: google.maps.Animation.DROP
	});

	infobox = new InfoBox({
		content: document.getElementById("infobox"),
		disableAutoPan: true,
		//maxWidth: 150,
		pixelOffset: new google.maps.Size(0, -50),
		zIndex: null,
		alignBottom: true,
		isHidden: false,
		//closeBoxMargin: "12px 4px 2px 2px",
		closeBoxURL: "images/infobox-close.png",
		closeBoxClass:"infoBox-close",
		infoBoxClearance: new google.maps.Size(1, 1)
	});

	openInfoBox(marker);

	google.maps.event.addListener(marker, 'click', function() {
		openInfoBox(this);
	});

	function openInfoBox(thisMarker){
		map.panTo(loc);
		map.panBy(0,-80);
		infobox.open(map, thisMarker);
	}

	var center;
	function calculateCenter() {
		center = map.getCenter();
	}
	google.maps.event.addDomListener(map, 'idle', function() {
		calculateCenter();
	});
	google.maps.event.addDomListener(window, 'resize', function() {
		map.setCenter(center);
	});

}
google.maps.event.addDomListener(window, 'load', initialize);