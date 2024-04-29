from math import radians, cos, sin, sqrt, atan2
def haversine(lat1, lon1, lat2, lon2):
    
    R = 6371.0

    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))
    lon1 = radians(float(lon1))
    lon1 = radians(float(lon2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1


    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))


    distance = R * c
    return distance

