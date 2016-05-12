var HASH_NAME = '';
var FILE_PATH = '';
var map;
var locations = [];
var locationMarkers = [];

var start = function() {
    loadFileNameAndCSVName();
    setMainTitle();
    if (HASH_NAME) {
        setupMap();
        loadLocations();
    }
}

var loadFileNameAndCSVName = function() {
    // Get html hash, example: www.dataviz.com#location would grab location
    if (window.location.hash.length > 0) {
		HASH_NAME = window.location.hash.substring(1);
	}
    if (HASH_NAME) {
        FILE_PATH = '../data/' + HASH_NAME + '.csv';
    }
};

var setMainTitle = function () {
    if (HASH_NAME) {
        $('#main-title').text(HASH_NAME);
    } else {
        $('#main-title').text('Please include #filename in the url to load your data');
    }
}

// Setup the leaflet map and legend;
var setupMap = function(){
	map = L.map('map').setView([0, 0], 5);

	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZHJ1c3RzbWkiLCJhIjoiTXV3RzNpNCJ9.44L5G1S6U6aPxFJeQnhmUQ', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
			'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="http://mapbox.com">Mapbox</a>',
		id: 'mapbox.light'
	}).addTo(map);
};

var drawLocations = function() {
	if (locations.length <= 0){
		// Load stores will callback drawStores when it's done, then run below code.
		loadLocations();
	} else {
  		locations.forEach(function(location){
			var icon = 'assets/icon_green.png';

			locationMarkers.push(L.marker([location.lat, location.lng])
				.setIcon(L.icon({iconUrl: icon}))
				.bindPopup(location.popoverInformation)
				.addTo(map));
		});
	}
};

var loadLocations = function(){
	d3.csv(FILE_PATH, function(rows){
		rows.forEach(function(d){
            // Popover information displays all the data in the row.
            locations.push({
				lat: +d.lat,
				lng: +d.lng,
                popoverInformation: JSON.stringify(d, null, "<br/>"),
			});
		});
        panMapToFirstLocationAndZoom();
		drawLocations();
	});
};

var panMapToFirstLocationAndZoom = function () {
    map.panTo(new L.LatLng(locations[0].lat, locations[0].lng));
    // TODO: make this zoom more accurate using a boundng box of the locations lat and lng
    map.setZoom(12);
};


// Code that runs on loading the js file
start();
