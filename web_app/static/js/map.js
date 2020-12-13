let map;
let renderer;

let relationshipsLayer = new L.featureGroup();
let shortestPathLayer = new L.featureGroup();
let citiesLayer = new L.featureGroup();
let satellitesLayer = new L.featureGroup();

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
        if (cities[i][0] === city) {
            const obj = cities[i].slice(1, 3);
            const div_icon = L.divIcon({ iconSize: [16, 16], className: 'city-icon' })
            const marker = L.marker(obj, { icon: div_icon }).bindPopup(cities[i][3]);
            citiesLayer.addLayer(marker);
        }
    }
    citiesLayer.addTo(map);
}

function drawCities() {
    const sel = GetSelectionValue();
    citiesLayer.clearLayers();
    for (let i = 0; i < cities.length; i++) {
        if (cities[i][0] === sel[0] || cities[i][0] === sel[1]) {
            const obj = cities[i].slice(1, 3);
            const div_icon = L.divIcon({ iconSize: [16, 16], className: 'city-icon' })
            const marker = L.marker(obj, { icon: div_icon }).bindPopup(cities[i][3]);
            citiesLayer.addLayer(marker);
        }
    }
    citiesLayer.addTo(map);
}

function drawSatellites() {
    satellitesLayer.clearLayers();
    for (let i = 0; i < sat_markers.length; i++) {
        const obj = sat_markers[i].slice(1, 3);
        const marker = L.circleMarker(obj, {
            renderer: renderer,
            radius: 4,
            weight: 0.5,
            color: '#BAB8BB',
            fillColor: '#FFB8AA',
            fillOpacity: 1.0,
        });
        satellitesLayer.addLayer(marker);
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
    relationshipsLayer.bringToBack();
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

function findSatellite(sat_id) {
    for (let i = 0; i < sat_markers.length; i++) {
        if (sat_id == sat_markers[i][0]) {
            return sat_markers[i].slice(1, 3);
        }
    }
}

function findCity(city_id) {
    for (let i = 0; i < cities.length; i++) {
        if (city_id == cities[i][0]) {
            return cities[i].slice(1, 3);
        }
    }
}

function drawShortestPath(sp_markers) {
    shortestPathLayer.clearLayers();
    for (let i = 0; i < sp_markers.length; i++) {
        const obj = sp_markers[i];
        let sat_one;
        let sat_two;
        if (i === 0) {
            if (obj[2] === 0) {
                sat_one = findCity(obj[1]);
                sat_two = findSatellite(obj[0]);
            } else {
                sat_one = findCity(obj[0]);
                sat_two = findSatellite(obj[1]);
            }
        } else if (i === sp_markers.length - 1) {
            if (obj[2] === 0) {
                sat_one = findCity(obj[1]);
                sat_two = findSatellite(obj[0]);
            } else {
                sat_one = findCity(obj[0]);
                sat_two = findSatellite(obj[1]);
            }
        } else {
            sat_one = findSatsat_one = findSatellite(obj[0]);
            sat_two = findCity(obj[1]);
            sat_two = findSatellite(obj[1]);
        }
        const satStart = [sat_one[0], sat_one[1]];
        const satEnd = [sat_two[0], sat_two[1]];
        latlngS = { 'lat': sat_one[0], 'lng': sat_one[1] };
        latlngE = { 'lat': sat_two[0], 'lng': sat_two[1] };
        let latlngs = [
            latlngS,
            latlngE
        ];
        if (Math.abs(sat_two[1] - sat_one[1]) > 180) {
            flipDirection = latlngs[1].lng < 0 ? -1 : 1;

            latlngs[0].lng = flipDirection * -179.9999999;
            latlngs[1].lng = flipDirection * 179.9999999;

            const intersection = math.intersect(satStart, satEnd, [90, 0], [-90, 0]);

            section1 = [
                [sat_one[0], sat_one[1]],
                [intersection[0], latlngs[0].lng]
            ];
            section2 = [
                [intersection[0], latlngs[1].lng],
                [sat_two[0], sat_two[1]]
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