let map;
let renderer;

let citiesLayer = new L.LayerGroup();
let satellitesLayer = new L.LayerGroup();
let relationshipsLayer = new L.LayerGroup();
let shortestPathLayer = new L.LayerGroup();

function initMapMollweide() {
    let crs = new L.Proj.CRS('ESRI:53009', '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +a=6371000 +b=6371000 +units=m +no_defs', {
        resolutions: [65536, 32768, 16384, 8192, 4096, 2048]
    });

    map = L.map('map', {
        renderer: L.canvas(),
        crs: crs,
        noWrap: true,
        minZoom: 1,
        maxZoom: 3,
        attributionControl: false,
        zoomControl: false
    });

    L.control.zoom({
        position: 'topright'
    }).addTo(map);
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

    let bounds = L.latLngBounds([
        [-70, -180],
        [80, 180]
    ]);
    map.setMaxBounds(bounds);

    map.on('drag', function() {
        map.panInsideBounds(bounds, { animate: false });
    });
}

async function createMap() {
    initMapMollweide();

    L.geoJson(countries, {
        style: {
            color: '#BAB8BB',
            weight: 0.5,
            opacity: 1,
            fillColor: '#FFFFFF',
            fillOpacity: 1
        }
    }).addTo(map);

    map.fitWorld();

    renderer = L.canvas({ padding: 0.5 });
}

function drawCity(city) {
    for (let i = 0; i < cities.length; i++) {
        if (cities[i][0] == city[0]) {
            const obj = cities[i].slice(1, 3);
            const div_circle = L.divIcon({ iconSize: [20, 20], className: 'circle' })
            const marker = L.marker(obj, { icon: div_circle }).bindPopup(cities[i][3]);
            citiesLayer.addLayer(marker);
        }
    }
    citiesLayer.addTo(map);
}

function drawCities() {
    const sel = GetSelectionValue();
    citiesLayer.clearLayers();
    for (let i = 0; i < cities.length; i++) {
        if (cities[i][0] == sel[0] || cities[i][0] == sel[1]) {
            const obj = cities[i].slice(1, 3);
            const div_circle = L.divIcon({ iconSize: [20, 20], className: 'circle' })
            const marker = L.marker(obj, { icon: div_circle }).bindPopup(cities[i][3]);
            citiesLayer.addLayer(marker);
        }
    }
    citiesLayer.addTo(map);
}

function drawSatellites() {
    satellitesLayer.clearLayers();
    for (let i = 0; i < sat_markers.length; i++) {
        const obj = sat_markers[i].slice(0, 2);
        const circle = L.circleMarker(obj, {
            renderer: renderer,
            radius: 4,
            weight: 0.5,
            color: '#BAB8BB',
            fillColor: '#FFB8AA',
            fillOpacity: 1.0
        });
        satellitesLayer.addLayer(circle);
    }
    satellitesLayer.addTo(map);
}

function drawRelationships() {
    relationshipsLayer.clearLayers();
    for (let i = 0; i < rel_markers.length; i++) {
        const obj = rel_markers[i];
        const satStart = [obj[0], obj[1]];
        const satEnd = [obj[2], obj[3]];
        latlngS = { 'lat': obj[0], 'lng': obj[1] };
        latlngE = { 'lat': obj[2], 'lng': obj[3] };
        let latlngs = [
            latlngS,
            latlngE
        ];

        if (Math.abs(obj[3] - obj[1]) > 180) {
            flipDirection = latlngs[1].lng < 0 ? -1 : 1;

            latlngs[0].lng = flipDirection * -179.9999999;
            latlngs[1].lng = flipDirection * 179.9999999;

            const intersection = math.intersect(satStart, satEnd, [90, 0], [-90, 0]);

            section1 = [
                [obj[0], obj[1]],
                [intersection[0], latlngs[0].lng]
            ];
            section2 = [
                [intersection[0], latlngs[1].lng],
                [obj[2], obj[3]]
            ];

            drawPolyRel(section1, '#BAB8BB');
            drawPolyRel(section2, '#BAB8BB');
            continue;
        }
        drawPolyRel(latlngs, '#BAB8BB');
    }
    relationshipsLayer.addTo(map);
}

function drawPolyRel(line, color) {
    const polyline = L.polyline(line, {
        renderer: renderer,
        color: color,
        opacity: 0.2,
        weight: 1,
        smoothFactor: 1
    }).addTo(map);
    relationshipsLayer.addLayer(polyline);
}

function drawShortestPath(sp_markers) {
    shortestPathLayer.clearLayers();
    for (let i = 0; i < sp_markers.length; i++) {
        const obj = sp_markers[i];
        const satStart = [obj[0], obj[1]];
        const satEnd = [obj[2], obj[3]];
        latlngS = { 'lat': obj[0], 'lng': obj[1] };
        latlngE = { 'lat': obj[2], 'lng': obj[3] };
        let latlngs = [
            latlngS,
            latlngE
        ];
        if (Math.abs(obj[3] - obj[1]) > 180) {
            flipDirection = latlngs[1].lng < 0 ? -1 : 1;

            latlngs[0].lng = flipDirection * -179.9999999;
            latlngs[1].lng = flipDirection * 179.9999999;

            const intersection = math.intersect(satStart, satEnd, [90, 0], [-90, 0]);

            section1 = [
                [obj[0], obj[1]],
                [intersection[0], latlngs[0].lng]
            ];
            section2 = [
                [intersection[0], latlngs[1].lng],
                [obj[2], obj[3]]
            ];

            drawPoly(section1, '#1EB76D');
            drawPoly(section2, '#1EB76D');
            continue;
        }
        drawPoly(latlngs, '#1EB76D');
    }
    shortestPathLayer.addTo(map);
}

function drawPoly(line, color) {
    const polyline = L.polyline(line, {
        renderer: renderer,
        color: color,
        opacity: 1.0,
        weight: 4,
        smoothFactor: 1
    }).addTo(map);
    shortestPathLayer.addLayer(polyline);
}

function focusView() {
    const sel = GetSelectionValue();
    let city1, city2;
    for (let i = 0; i < cities.length; i++) {
        if (cities[i][0] === sel[0]) {
            city1 = cities[i];
        } else if (cities[i][0] === sel[1]) {
            city2 = cities[i];
        }
    }
    const focus = [(city1[1] + city2[1]) / 2, (city1[2] + city2[2]) / 2];
    let zoom = 2;
    if ((Math.abs(city1[1] - city2[1]) >= 50) || (Math.abs(city1[2] - city2[2]) >= 80)) {
        zoom = 1;
    }
    map.setView(focus, zoom);
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