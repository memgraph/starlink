var map;
var myRenderer;

var cities = [];
var opticalPaths;

var citiesLayer = new L.LayerGroup();
var satellitesLayer = new L.LayerGroup();
var relationshipsLayer = new L.LayerGroup();
var shortestPathLayer = new L.LayerGroup();

var json_satellites;
var json_relationships;
var json_shortest_path;

var sat_markers;
var firstSatellite;

var firstDropdown;
var secondDropdown;
var removedItemDropdownOne;
var removedItemDropdownTwo;

var simStopped = true;
var nextButtonStart = true;
var dropdownOneSelected = false;
var dropdownTwoSelected = false;
var selectedCities;
var xhr;


function simulation() {
    if (nextButtonStart) {
        document.getElementById("startStopButton").disabled = true;
        simulationStarted();
        nextButtonStart = false;
    } else {
        document.getElementById("startStopButton").disabled = true;
        simulationStopped();
        nextButtonStart = true;
        document.getElementById("startStopButton").disabled = false;
    }
}

async function simulationStarted() {
    simStopped = false;

    document.getElementById("startStopButton").innerHTML = "Stop simulation";

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

    document.getElementById("startStopButton").innerHTML = "Start simulation";

    $('#dropdownOne').prop('disabled', false);
    $('#dropdownTwo').prop('disabled', false);

    document.getElementById('initial-stats').style.display = 'initial';
    document.getElementById('stats').style.display = 'none';

    drawCities();
    map.dragging.enable();
    map.touchZoom.enable();
    map.doubleClickZoom.enable();
    map.scrollWheelZoom.enable();
    map.boxZoom.enable();
    map.keyboard.enable();
    if (map.tap) map.tap.enable();
    document.getElementById('map').style.cursor = 'grab';

    if (xhr != null) {
        xhr.abort()
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function userAborted(xhr) {
    return !xhr.getAllResponseHeaders();
}