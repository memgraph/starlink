let nextButtonStart = true;

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
    drawSatellites();
    drawRelationships(rel_markers);
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