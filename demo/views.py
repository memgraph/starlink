from django.http import HttpResponse
from demo.database import Memgraph
import demo.data.db_operations as db_operations


def index(request):

    db = Memgraph()
    satellites = db_operations.import_all_satellites(db)
    cities = db_operations.import_all_cities(db)

    sat_markers = []
    city_markers = []

    for sat in satellites:
        s = sat['n']
        #print(s.properties)
        marker = [s.properties['x'], s.properties['y']]
        sat_markers.append(marker)

    for city in cities:
        c = city['n']
        #print(c.properties)
        marker = [c.properties['x'], s.properties['y']]
        city_markers.append(marker)

    #print(sat_markers)
    #print(city_markers)

    html = """<html>
    <head>
        <link rel='stylesheet' href='https://unpkg.com/leaflet@1.6.0/dist/leaflet.css' />
        <script src='https://unpkg.com/leaflet@1.6.0/dist/leaflet.js'></script>
        <style>
            #map {position: absolute; top: 0; bottom:0; left:0; right: 0}
        </style>
    </head>
    <body>
        <div id = "map"></div>
        <script>
            var map = L.map('map').setView([0,0], 1);
            L.tileLayer("https://api.maptiler.com/maps/basic/{z}/{x}/{y}.png?key=cYtmZZ4gfz1cXNCBs8r4",{
                attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
            }).addTo(map);
            var mark;
            for (mark in city_markers){
                var marker = L.marker(mark).addTo(map);
            }
            
        </script>
    </body>
</html>
    """

    return HttpResponse(html)