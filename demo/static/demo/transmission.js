function transmission_time(sp_markers){
    total_transmission_time = 0;
    for (var i = 0; i < sp_markers.length; i++) {
        total_transmission_time = total_transmission_time + sp_markers[i][4];
        //console.log(sp_markers[i][4]);
    }
    return "Transmission time: " + total_transmission_time;
}

function optic_cable_time(){
    

}