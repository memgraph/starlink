var map;
var cities;
var opticalPaths;
var simStopped = true;
var citiesLayer = new L.LayerGroup();
var satellitesLayer = new L.LayerGroup();
var relationshipsLayer = new L.LayerGroup();
var shortestPathLayer = new L.LayerGroup();
var json_satellites;
var json_relationships;
var json_shortest_path;
var removedItemDropdownOne;
var removedItemDropdownTwo;
var myRenderer;
var pane;

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

cities = JSON.parse("{{city_markers|escapejs}}");
opticalPaths = JSON.parse("{{op_markers|escapejs}}");

var firstDropdown = document.getElementById("dropdownOne");
var secondDropdown = document.getElementById("dropdownTwo");

populateDropdowns();

initDropdowns();

$(document).ready(function () {
    idleFunction();
})

function idleFunction() {
    simStopped = true;

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

function ajaxCall() {
    var xhr = $.ajax({
        type: 'GET',
        url: "{% url 'json_satellites_and_relationships' %}",
        data: {
            cityOne: document.getElementById("dropdownOne").options[document.getElementById("dropdownOne").selectedIndex].value,
            cityTwo: document.getElementById("dropdownTwo").options[document.getElementById("dropdownTwo").selectedIndex].value,
            "json_satellites": json_satellites,
            "json_relationships": json_relationships,
            "json_shortest_path": json_shortest_path
        },
        async: true,
        success: function (data) {
            drawCities();
            drawRelationships(JSON.parse(data.json_relationships));
            drawSatellites(JSON.parse(data.json_satellites));

            if (data.json_shortest_path.length != 0) {
                drawShortestPath(JSON.parse(data.json_shortest_path));
                document.getElementById("ttime").innerHTML = "Satellite communication: " + transmission_time(JSON.parse(data.json_shortest_path));
                selectedCities = GetSelectionText();
                document.getElementById("optic").innerHTML = "Fiber-optic cable communication: " + optical_time(opticalPaths, selectedCities[0], selectedCities[1]);
            } else {
                shortestPathLayer.clearLayers();
                document.getElementById("ttime").innerHTML = "No visible satellites.";
                selectedCities = GetSelectionText();
                document.getElementById("optic").innerHTML = "Fiber-optic cable communication: " + optical_time(opticalPaths, selectedCities[0], selectedCities[1]);
            }
        },
        error: function (thrownError) {
            alert(thrownError);
        }
    });
};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function runSimulation() {
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

    while (true) {
        if (simStopped) {
            relationshipsLayer.clearLayers();
            satellitesLayer.clearLayers();
            shortestPathLayer.clearLayers();
            document.getElementById("ttime").innerHTML = "";
            document.getElementById("optic").innerHTML = "";
            break;
        }
        ajaxCall();
        await sleep(1000);
    }
}

function showMapAlert(message, alertType) {
    $('#map-alert').html("<div class='alert card-text alert-" + alertType + "'>" + message + "</div>");
    $('#map-alert').show();
}

function showTransmissionTimeAlert(message, alertType) {
    $('#tt-alert').html("<div class='alert card-text alert-" + alertType + "'>" + message + "</div>");
    $('#tt-alert').show();
}