# from urllib.request import urlopen
from audioop import add
import json 
import os 
import urllib
import requests 

AUTH_KEY_GEOCODING = os.environ['AUTH_KEY_GEOCODING']
AUTH_KEY_DISTANCE_MATRIX = os.environ['AUTH_KEY_DISTANCE_MATRIX']

BASE_URL_GEOCODING = "https://maps.googleapis.com/maps/api/geocode/json?"
BASE_URL_DISTANCE_MATRIX = "https://maps.googleapis.com/maps/api/distancematrix/json?"

# decorator function for caching calls to json, create json if it doesnt exist
def cache_json(func):
    def wrapper(*args, **kwargs):
        # if .cache doesnt exist, create it
        if not os.path.exists(".cache"):
            os.makedirs(".cache")
    
        filename = os.path.join('.cache',f"{func.__name__}.json")
        key = str((args, kwargs))
        if os.path.exists(filename):
            with open(filename, "r") as f:
                cache = json.load(f)

            if key in cache:
                return cache[key]
            else: 
                val = func(*args, **kwargs)
                with open(filename, "w") as f:
                    json.dump({**cache, key : val}, f)
                return val

        else:
            val = func(*args, **kwargs)
            with open(filename, "w") as f:
                json.dump({key: val}, f)
            
            return val 

        
        # if os.path.exists(filename):
        #     with open(filename, "r") as f:
        #         cache = json.load(f)
        # else:
        #     data = func(*args, **kwargs)
        #     with open(filename, "w") as f:
        #         json.dump(data, f)
        #     return data
        
    return wrapper

@cache_json
def get_distance_matrix(orig_coord, dest_coord):
    orig_coord = (str(orig_coord[0]), str(orig_coord[1]))
    dest_coord = (str(dest_coord[0]), str(dest_coord[1]))
    parameters = {"origins": ','.join(orig_coord),
                  "destinations": ','.join(dest_coord),
                  "mode": "driving",
                  "language": "en-EN",
                  "sensor": "false",
                  "key": AUTH_KEY_DISTANCE_MATRIX}
    r = requests.get(f"{BASE_URL_DISTANCE_MATRIX}{urllib.parse.urlencode(parameters)}")
    data = json.loads(r.content)    
    return data

def get_driving_time(orig_coord, dest_coord):
    return get_distance_matrix(orig_coord, dest_coord)['rows'][0]['elements'][0]['duration']['value']

@cache_json
def get_geocoding(address):
    parameters = {"address": address,
                  "key": AUTH_KEY_GEOCODING}
    r = requests.get(f"{BASE_URL_GEOCODING}{urllib.parse.urlencode(parameters)}")
    data = json.loads(r.content)
    return data

def get_coordinates(address):
    return get_geocoding(address)['results'][0]['geometry']['location']

def get_formatted_address(address):
    return get_geocoding(address)['results'][0]['formatted_address']

    # print(get_geocoding(address))
    # print('hii 0----------------------------------------------------')
    # return get_geocoding(address)

