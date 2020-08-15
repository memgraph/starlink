function initMapMollweide() {
    var crs = new L.Proj.CRS('ESRI:53009', '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +a=6371000 +b=6371000 +units=m +no_defs', {
        resolutions: [65536, 32768, 16384, 8192, 4096, 2048]
    });

    map = L.map('map', {
        renderer: L.canvas(),
        crs: crs,
        noWrap: true,
        minZoom: 1,
        maxZoom: 3,
        attributionControl: false
    });
}

function initMapMercator() {
    map = L.map('map', {
        zoom: 3,
        center: [15, -5],
        layers: [citiesLayer],
        attributionControl: false
    });
    L.tileLayer("https://api.maptiler.com/maps/basic/{z}/{x}/{y}.png?key=cYtmZZ4gfz1cXNCBs8r4", {
        attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
        noWrap: true,
        maxZoom: 5,
        minZoom: 1,
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
            var marker = L.circleMarker(obj,
                {
                    renderer: myRenderer,
                    color: '#7a0099',
                    fillColor: '#f03',
                    radius: 7
                }
            ).bindPopup(cities[i][3]);
            citiesLayer.addLayer(marker);
        }
    }
    citiesLayer.addTo(map);
}

function drawSatellites() {
    satellitesLayer.clearLayers();
    for (var i = 0; i < sat_markers.length; i++) {
        var obj = sat_markers[i].slice(0, 2);
        var circle = L.circleMarker(obj, {
            renderer: myRenderer,
            color: '#FF7F50',
            fillColor: '#f03',
            fillOpacity: 0.5,
            radius: 2
        });
        satellitesLayer.addLayer(circle);
    }
    if (simStopped) return;
    satellitesLayer.addTo(map);
}

function drawRelationships(rel_markers) {
    relationshipsLayer.clearLayers();
    for (var i = 0; i < rel_markers.length; i++) {
        var obj = rel_markers[i];
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

            drawPolyRel(section1, '#bfbfbf', relationshipsLayer);
            drawPolyRel(section2, '#bfbfbf', relationshipsLayer);
            continue;
        }
        drawPolyRel(latlngs, '#bfbfbf', relationshipsLayer);

    }
    if (simStopped) return;
    relationshipsLayer.addTo(map);
}

function drawPoly(line, colour, layer) {
    var polyline = L.polyline(line, {
        renderer: myRenderer,
        color: colour,
        opacity: 0.8,
        weight: 2.5,
        smoothFactor: 1
    }).addTo(map);
    layer.addLayer(polyline);
}

function drawPolyRel(line, colour, layer) {
    var polyline = L.polyline(line, {
        renderer: myRenderer,
        color: colour,
        opacity: 0.2,
        weight: 1,
        smoothFactor: 1
    }).addTo(map);
    layer.addLayer(polyline);
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

            drawPoly(section1, '#7a0099', shortestPathLayer);
            drawPoly(section2, '#7a0099', shortestPathLayer);
            continue;
        }
        drawPoly(latlngs, '#7a0099', shortestPathLayer);
    }
    if (simStopped) return;
    shortestPathLayer.addTo(map);
}

function focusView() {
    var sel = GetSelectionValue();
    var city1, city2;
    for (var i = 0; i < cities.length; i++) {
        if (cities[i][0] === sel[0]) {
            city1 = cities[i];
        } else if (cities[i][0] === sel[1]) {
            city2 = cities[i];
        }
    }
    var focus = [(city1[1] + city2[1]) / 2, (city1[2] + city2[2]) / 2];
    var zoom = 2;
    if ((Math.abs(city1[1] - city2[1]) >= 50) || (Math.abs(city1[2] - city2[2]) >= 80)) {
        zoom = 1;
    }
    map.setView(focus, zoom);
}

function showMapAlert(message, alertType) {
    $('#map-alert').html("<div class='alert card-text " + alertType + "'>" + message + "</div>");
    $('#map-alert').show();
}

function showTransmissionTimeAlert(message, alertType) {
    $('#tt-alert').html("<div class='card-header " + alertType + "'>" + message + "</div>");
    $('#tt-alert').show();
}

function newDataLoaded() {
    if (firstSatellite == undefined) {
        return true;
    }
    newFirstSatellite = sat_markers[0].slice(0, 2);
    if (newFirstSatellite[0] != firstSatellite[0]) {
        return true;
    } else {
        return false;
    }
}