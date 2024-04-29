import requests
import gtfs_realtime_pb2
import sqlite3
import collections
import haversine
from dj import Dijkstra
from dj import convert_to_desired_format
#import dj
# 实时数据API URL配置
API_URLS = {
    'subway': {
        'subway_ace': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace',
        'subway_bdfm': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm',
        'subway_g': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g',
        'subway_jz': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz',
        'subway_nqrw': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw',
        'subway_l': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l',
        'subway_1234567': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs',
        'subway_si': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si'
    },
    'lirr': {
        'lirr': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/lirr%2Fgtfs-lirr'
    },
    'metronorth': {
        'metro_north': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/mnr%2Fgtfs-mnr'
    },
    'service_alerts': {
        'service_alerts_all': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fall-alerts',
        'service_alerts_subway': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts',
        'service_alerts_bus': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fbus-alerts',
        'service_alerts_lirr': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Flirr-alerts',
        'service_alerts_metro_north': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fmnr-alerts'
    }
}

def fetch_and_parse_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def update_data():
    data = {}
    for category, urls in API_URLS.items():
        data[category] = {}
        for key, url in urls.items():
            feed = fetch_and_parse_data(url)
            if feed:
                data[category][key] = feed
    return data

def get_static_data():

    try:

        conn = sqlite3.connect('db/database.db')
        conn.row_factory = sqlite3.Row  
        cursor = conn.cursor()


        cursor.execute('SELECT * FROM routes')
        routes = cursor.fetchall() 


        cursor.execute('SELECT * FROM stops')
        stops = cursor.fetchall()  


        routes_dict = [dict(ix) for ix in routes]
        stops_dict = [dict(ix) for ix in stops]

        conn.close()

        return {'routes': routes_dict, 'stops': stops_dict}

    except sqlite3.Error as e:
        print(f"data error: {e}")
        return None
    except Exception as e:
        print(f"normal error: {e}")
        return None

def combine_data():
    real_time_data = update_data()
    static_data = get_static_data()
    
    return {'real_time': real_time_data, 'static': static_data}

def g():
    static_data = get_static_data()["stops"]
    graph=collections.defaultdict(list)
    d=collections.defaultdict(list)
    for stop in static_data:
        d[stop["stop_id"]].append([stop["stop_lat"],stop["stop_lon"]])
    for stop in static_data:
        if stop["parent_station"]:
            lat1,lon1=stop["stop_lat"],stop["stop_lon"]
            lat2,lon2=d[stop["parent_station"]][0][0],d[stop["parent_station"]][0][1]
            #for parent in stop["parent_station"]:
                #print(stop["parent_station"])
            graph[stop["parent_station"]].append([stop["stop_id"],haversine.haversine(lat1, lon1, lat2, lon2)])
    return graph,d


def dijkstra_algorithm():
    graph,d=g()
    graph=convert_to_desired_format(graph)
    dijkstra = Dijkstra(graph)
    for stop in d.keys():
        if stop not in graph:
            graph[stop]={}
    
    source,destination=str(input()),str(input())
    path_length, path = dijkstra.find_shortest_path(source,destination)
    print(f"Shortest path length from {source} to {destination}: {path_length}")
    dijkstra.remove_station('101N')
    
    path_length, path = dijkstra.find_shortest_path(source,destination)
    print(f"Shortest path length from {source} to {destination}: {path_length}")


