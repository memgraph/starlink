var map;
var myRenderer;

var cities;
var opticalPaths;

var citiesLayer = new L.LayerGroup();
var satellitesLayer = new L.LayerGroup();
var relationshipsLayer = new L.LayerGroup();
var shortestPathLayer = new L.LayerGroup();

var json_satellites;
var json_relationships;
var json_shortest_path;

var firstDropdown;
var secondDropdown;
var removedItemDropdownOne;
var removedItemDropdownTwo;

var simStopped = true;


async function createMap() {
    initMapMollweide();

    L.geoJson(countries, {
        style: {
            color: '#000',
            weight: 0.5,
            opacity: 1,
            fillColor: '#fff',
            fillOpacity: 1
        }
    }).addTo(map);

    map.fitWorld();

    myRenderer = L.canvas({ padding: 0.5 });
}

async function simulationStarted() {
    simStopped = false;

    $('#startButton').prop('disabled', true);
    $('#stopButton').prop('disabled', false);

    $('#dropdownOne').prop('disabled', true);
    $('#dropdownTwo').prop('disabled', true);

    map.dragging.disable();
    map.touchZoom.disable();
    map.doubleClickZoom.disable();
    map.scrollWheelZoom.disable();
    map.boxZoom.disable();
    map.keyboard.disable();
    if (map.tap) map.tap.disable();

    document.getElementById('map').style.cursor = 'default';

    showMapAlert('Simulation is running...', 'warning');

    while (!simStopped) {
        ajaxCall();
        await sleep(1000);
    }
}

function simulationStopped() {
    simStopped = true;

    relationshipsLayer.clearLayers();
    satellitesLayer.clearLayers();
    shortestPathLayer.clearLayers();
    document.getElementById("ttime").innerHTML = "";
    document.getElementById("optic").innerHTML = "";

    $('#stopButton').prop('disabled', true);
    $('#startButton').prop('disabled', false);

    $('#dropdownOne').prop('disabled', false);
    $('#dropdownTwo').prop('disabled', false);

    drawCities();
    map.dragging.enable();
    map.touchZoom.enable();
    map.doubleClickZoom.enable();
    map.scrollWheelZoom.enable();
    map.boxZoom.enable();
    map.keyboard.enable();
    if (map.tap) map.tap.enable();
    document.getElementById('map').style.cursor = 'grab';

    showMapAlert('Choose cities and start the simulation!', 'info');
    showTransmissionTimeAlert('Transmission time for satellite communication and fiber-optic cable', 'info');
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}