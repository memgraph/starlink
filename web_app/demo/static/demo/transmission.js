function transmission_time(sp_markers) {
    let total_transmission_time = 0;

    for(sp of sp_markers){
        total_transmission_time += sp[4];
    }
    return `${Math.round((total_transmission_time * 1000 + Number.EPSILON) * 100) / 100} ms`;
}

function optical_time(opticalPaths, city1, city2) {

    for(op of opticalPaths){
        let city1Found = (city1 == op[0] || city1 == op[1]);
        let city2Found = (city2 == op[0] || city2 == op[1]);
    
        if(city1Found && city2Found) return `${op[2]} ms`;
    }
    return 'No data found for selected cities.';
}

function createTransmissionTimeCard() {
    showTransmissionTimeAlert('Transmission time for satellite communication and fiber-optic cable', '');
}