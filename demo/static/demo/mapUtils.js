function initMap() {
    map = L.map('map', { zoom: 3, center: [30, 0], layers: [citiesLayer], attributionControl: false });
    L.tileLayer("https://api.maptiler.com/maps/basic/{z}/{x}/{y}.png?key=cYtmZZ4gfz1cXNCBs8r4", {
        attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
        noWrap: true,
        maxZoom: 5,
        minZoom: 1
    }).addTo(map);

    var bounds = L.latLngBounds([[-70, -180], [80, 180]]);
    map.setMaxBounds(bounds);

    map.on('drag', function () {
        map.panInsideBounds(bounds, { animate: false });
    });
}

function drawCities() {
    var sel = GetSelectionValue();
    citiesLayer.clearLayers();
    for (var i = 0; i < cities.length; i++) {
        if (cities[i][0] == sel[0] || cities[i][0] == sel[1]) {
            var obj = cities[i].slice(1, 3);
            var marker = (L.marker(obj).bindTooltip(cities[i][3],
                {
                    permanent: false,
                    direction: "left"
                }
            ));
            citiesLayer.addLayer(marker);
        }
    }
    focusView();
    citiesLayer.addTo(map);
}

function drawSatellites(sat_markers) {
    satellitesLayer.clearLayers();
    for (var i = 0; i < sat_markers.length; i++) {
        var obj = sat_markers[i].slice(0, 2);
        var circle = L.circle(obj, {
            color: '#FF7F50',
            fillColor: '#f03',
            fillOpacity: 0.5,
            radius: 1000
        });
        satellitesLayer.addLayer(circle);
    }
    satellitesLayer.addTo(map);
}

function drawRelationships(rel_markers) {
    relationshipsLayer.clearLayers();
    for (var i = 0; i < rel_markers.length; i++) {
        var obj = rel_markers[i];
        if (!(obj[1] < -50 && obj[3] > 50) && !(obj[3] < -50 && obj[1] > 50)) {
            var satStart = [obj[0], obj[1]];
            var satEnd = [obj[2], obj[3]];
            var latlngs = [
                satStart,
                satEnd
            ];
            var polyline = L.polyline(latlngs, {
                color: 'lightgray', opacity: 0.1, weight: 1, smoothFactor: 1
            }).addTo(map);
            relationshipsLayer.addLayer(polyline);
        }
    }
   relationshipsLayer.addTo(map);
}

function drawPoly(line) {
    var polyline = L.polyline(line, {
        color: '#483D8B', opacity: 0.8, weight: 2.5, smoothFactor: 1
    }).addTo(map);
    shortestPathLayer.addLayer(polyline);
}

function drawShortestPath(sp_markers) {
    shortestPathLayer.clearLayers();

    for (var i = 0; i < sp_markers.length; i++) {
        var obj = sp_markers[i];
        var satStart = [obj[0], obj[1]];
        var satEnd = [obj[2], obj[3]];
        latlngS = { 'lat': obj[0], 'lng': obj[1] };
        latlngE = { 'lat': obj[2], 'lng': obj[3] };
        var latlngs = [
            latlngS,
            latlngE
        ];
        if (Math.abs(obj[3] - obj[1]) > 180) {
            flipDirection = latlngs[1].lng < 0 ? -1 : 1;

            latlngs[0].lng = flipDirection * -179.9999999;
            latlngs[1].lng = flipDirection * 179.9999999;

            var intersection = math.intersect(satStart, satEnd, [90, 0], [-90, 0]);

            section1 = [[obj[0], obj[1]], [intersection[0], latlngs[0].lng]];
            section2 = [[intersection[0], latlngs[1].lng], [obj[2], obj[3]]];

            drawPoly(section1);
            drawPoly(section2);
            continue;
        }
        drawPoly(latlngs);
    }
    shortestPathLayer.addTo(map);
}

function focusView(){
    var sel = GetSelectionValue();
    var city1, city2;
    for (var i = 0; i < cities.length; i++) {
        if (cities[i][0] === sel[0]) {
            city1 = cities[i];
        } else if (cities[i][0] === sel[1]){
            city2 = cities[i];
        }
    }
    console.log(city1, city2);
    var focus = [(city1[1] + city2[1])/2, (city1[2] + city2[2])/2];
    map.setView(focus, 3);
}
