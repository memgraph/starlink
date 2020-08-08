function transmission_time(sp_markers){
    total_transmission_time = 0;
    for (var i = 0; i < sp_markers.length; i++) {
        total_transmission_time = total_transmission_time + sp_markers[i][4];
    }
    return (Math.round((total_transmission_time*1000 + Number.EPSILON) * 100) / 100) + " ms";
}

function optical_time(opticalPaths, city1, city2){

    for(var i = 0; i < opticalPaths.length; i++){
        if(city1 == opticalPaths[i][0] || city1 == opticalPaths[i][1]){
            if(city2 == opticalPaths[i][0] || city2 == opticalPaths[i][1] ){
                return opticalPaths[i][2] + " ms";
            }
        }
    }

    return "no data found for selected cities."
}