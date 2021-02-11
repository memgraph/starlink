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

function drawCity(id) {
    const obj = city_markers[id];
    const div_icon = L.divIcon({ iconSize: [16, 16], className: 'city-icon' })
    const marker = L.marker(obj, { icon: div_icon }).bindPopup(city_names[id]);
    citiesLayer.addLayer(marker);
    citiesLayer.addTo(map);
}

function drawCities() {
    const sel = GetSelectionValue();
    citiesLayer.clearLayers();
    drawCity(sel[0]);
    drawCity(sel[1]);
}

function drawSatellites() {
    satellitesLayer.clearLayers();
    for (let id in sat_markers) {
        const obj = sat_markers[id];
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

function drawShortestPath(sp_markers) {
    shortestPathLayer.clearLayers();
    for (let i = 0; i < sp_markers.length; i++) {
        const obj = sp_markers[i];
        let sat_one;
        let sat_two;
        if (i === 0 || i === sp_markers.length - 1) {
            if (obj[2] === 0) {
                sat_one = city_markers[obj[1]];
                sat_two = sat_markers[obj[0]];
            } else {
                sat_one = city_markers[obj[0]];
                sat_two = sat_markers[obj[1]];
            }
        } else {
            sat_one = sat_markers[obj[0]];
            sat_two = sat_markers[obj[1]];
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
    let city1 = city_markers[sel[0]];
    let city2 = city_markers[sel[1]];

    const focus = [(city1[0] + city2[0]) / 2, (city1[1] + city2[1]) / 2];
    let zoom = 2;
    if ((Math.abs(city1[0] - city2[0]) >= 50) || (Math.abs(city1[1] - city2[1]) >= 80)) {
        zoom = 1;
    }
    map.setView(focus, zoom);
}

function newDataLoaded() {
    if (firstSatellite == undefined) {
        return true;
    }
    newFirstSatellite = sat_markers[Object.keys(sat_markers)[0]];
    if (newFirstSatellite[0] != firstSatellite[0]) {
        return true;
    } else {
        return false;
    }
}