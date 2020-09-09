let simStopped = true;

let json_satellites;
let json_relationships;
let json_shortest_path;
let firstSatellite;

let selectedCities;

async function postData(url = '') {
    const response = await fetch(url, {
        method: 'GET'
    });
    return response.json();
}

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
        await postData(`${window.origin}/` + 'json_satellites_and_relationships?cityOne=' + firstDropdown.options[firstDropdown.selectedIndex].value +
                '&cityTwo=' + secondDropdown.options[secondDropdown.selectedIndex].value)
            .then(data => {
                sat_markers = JSON.parse(data.json_satellites);
                rel_markers = JSON.parse(data.json_relationships);
                if (!simStopped && newDataLoaded()) {
                    drawCities();
                    firstSatellite = sat_markers[0].slice(0, 2);
                    drawRelationships();
                    drawSatellites();
                    document.getElementById('initial-stats').style.display = 'none';
                    document.getElementById('stats').style.display = 'initial';
                    if (data.json_shortest_path.length != 0) {
                        shortestPathLayer.clearLayers();
                        drawShortestPath(JSON.parse(data.json_shortest_path));
                        document.getElementById("ttime").innerHTML = `Satellite latency: <strong class="text-primary">${transmission_time(JSON.parse(data.json_shortest_path))} </strong>`;
                        selectedCities = GetSelectionText();
                        document.getElementById("optic").innerHTML = `Fiber-optic cable latency: <strong class="text-primary">${optical_time(opticalPaths, selectedCities[0], selectedCities[1])}</strong>`;
                    } else {
                        shortestPathLayer.clearLayers();
                        document.getElementById("ttime").innerHTML = `No visible satellites.`;
                        selectedCities = GetSelectionText();
                        document.getElementById("optic").innerHTML = `Fiber-optic cable latency: <strong class="text-primary">${optical_time(opticalPaths, selectedCities[0], selectedCities[1])}</strong>`;
                    }
                    document.getElementById("startStopButton").disabled = false;
                }
            }).catch(err => {
                console.error('There was an error!', err);
            });
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
}